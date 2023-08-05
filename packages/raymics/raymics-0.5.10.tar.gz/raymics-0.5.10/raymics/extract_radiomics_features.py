import os
import re
import math
import json
import logging
import argparse
import base64
import tqdm
import imageio.v3 as iio
import numpy as np
import pandas as pd
import cv2
import SimpleITK as sitk
import PIL
import PIL.Image
import PIL.ImageDraw
import string
import tempfile
import dicom2nifti
import traceback

from typing import List, Union, Tuple
from multiprocessing import Manager, Pool
from collections import OrderedDict
from radiomics.featureextractor import RadiomicsFeatureExtractor
from raymics import DatasetType
from raymics.constants import COL_LABEL, RADIOMIC_FEATURE_FILENAME, COL_INDEX, \
    FILENAME_ANNOTATION, COL_DATA_PATH, COL_MASK_PATH, COL_ID
from raymics.dataset import Dataset, LabeledDataset
from raymics.utils import is_image, is_video, is_ndarray, is_labelme, \
    is_dicom_folder, isBase64
from raymics.log import logger
from radiomics.featureextractor import logger as rlogger
rlogger.setLevel(logging.ERROR)

GROUP_LEN = 100


def pop_unnamed(df: pd.DataFrame) -> pd.DataFrame:
    unnamed_cols = [col for col in df.columns if col.startswith("Unnamed")]
    for col in unnamed_cols:
        df.pop(col)
    return df


def dummy_mask(shape: Tuple[int, int]) -> sitk.Image:
    mask = np.ones(shape=shape)
    mask[0, 0] = 0
    mask = sitk.GetImageFromArray(mask)
    return mask


def cv_img2sitk_image(path: str) -> sitk.Image:
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = sitk.GetImageFromArray(img)
    return img


def ndarray2sitk_image(path: str) -> sitk.Image:
    """ndarray of gray image or opencv image"""
    img = np.load(path)
    assert len(img.shape) in [2, 3], f"Not 2D data: {path}"
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = sitk.GetImageFromArray(img)
    return img


def shape_to_mask(img_shape: Tuple[int, int], points: List[Tuple[float, float]],
                  shape_type: str = None, line_width: int = 10,
                  point_size: int = 5) -> np.ndarray:
    mask = np.zeros(img_shape[:2], dtype=np.uint8)
    mask = PIL.Image.fromarray(mask)
    draw = PIL.ImageDraw.Draw(mask)
    xy = [tuple(point) for point in points]

    if shape_type == "circle":
        assert len(xy) == 2, "Shape of shape_type=circle must have 2 points"
        (cx, cy), (px, py) = xy
        d = math.sqrt((cx - px) ** 2 + (cy - py) ** 2)
        draw.ellipse([cx - d, cy - d, cx + d, cy + d], outline=1, fill=1)

    elif shape_type == "rectangle":
        assert len(xy) == 2, "Shape of shape_type=rectangle must have 2 points"
        draw.rectangle(xy, outline=1, fill=1)

    elif shape_type == "line":
        assert len(xy) == 2, "Shape of shape_type=line must have 2 points"
        draw.line(xy=xy, fill=1, width=line_width)

    elif shape_type == "linestrip":
        draw.line(xy=xy, fill=1, width=line_width)

    elif shape_type == "point":
        assert len(xy) == 1, "Shape of shape_type=point must have 1 points"
        cx, cy = xy[0]
        r = point_size
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=1, fill=1)

    else:
        assert len(xy) > 2, "Polygon must have points more than 2"
        draw.polygon(xy=xy, outline=1, fill=1)

    mask = np.array(mask)

    return mask


def labelme_json2mask(path) -> sitk.Image:
    with open(path) as f:
        json_data = json.load(f)

    points = json_data["shapes"][0]["points"]
    shape = json_data["shapes"][0]["shape_type"]
    h, w = json_data["imageHeight"], json_data["imageWidth"]
    mask = shape_to_mask(img_shape=(h, w), points=points, shape_type=shape)
    mask = sitk.GetImageFromArray(mask)
    return mask


def get_mask(mask_path: Union[str, None], shape: Tuple[int, int]) -> sitk.Image:
    # no mask
    if mask_path is None:
        mask = dummy_mask(shape=shape)

    # numpy.ndarray
    elif is_ndarray(mask_path):
        mask = ndarray2sitk_image(mask_path)

    # opencv image
    elif is_image(mask_path):
        mask = cv_img2sitk_image(mask_path)

    # labelme json
    elif is_labelme(mask_path):
        mask = labelme_json2mask(mask_path)

    # try to read mask using SimpleITK - raise error if wrong file is supplied
    else:
        mask = sitk.ReadImage(mask_path)

    return mask


def check_data(paths: Union[str, List[str]]) -> int:
    """

    Parameters
    ----------
    paths : List of data paths

    Returns
    -------
    0 : 2D or 3D, not time series
    1 : Video, time series
    2 : Error, mix includes 0, 1

    """
    # video_paths = [p for p in paths if len(FFProbe(p).video)]
    if isinstance(paths, str):
        paths = [paths]

    video_paths = [p for p in paths if is_video(p)]
    if video_paths:
        if len(video_paths) == len(paths):
            return DatasetType.TS
        else:
            raise Exception("It is supposed only time series data or"
                            " non-time series data in the paths.")
    else:
        return DatasetType.NON_TS


def convert_to_rel_paths(paths: List[str], root_dir: str) -> List[str]:
    # todo
    return paths


def rename_duplicate_path(path: str) -> str:
    p, ext = os.path.splitext(path)
    if re.match(".+_\d", os.path.basename(p)):
        splits = p.split("_")
        seq = int(splits[-1])
        new_path = "_".join(splits[:-1]) + f"_{seq + 1}" + ext
    else:
        new_path = p + "_1" + ext

    return rename_duplicate_path(new_path) \
        if os.path.exists(new_path) else new_path


def read_mask(mask_path: str) -> sitk.Image:
    """
    Parameters
    ----------
    mask_path : str
        Path of the mask file.

    """
    ext = os.path.splitext(mask_path)[-1].lower()
    ext = ext[1:] if ext.startswith(".") else ext
    if is_image(mask_path):
        mask = cv2.imread(mask_path)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        mask = sitk.GetImageFromArray(mask)
    elif ext == "npy":
        mask = np.load(mask_path)
        mask = sitk.GetImageFromArray(mask)
    else:
        raise ValueError(f"Mask with extension '{ext}' is not supported!")

    return mask


def extract_non_ts(data_idxs: List[int],
                   data_ids: List,
                   data_paths: List[str],
                   mask_paths: List[str],
                   result_labels_path: str,
                   extractor: RadiomicsFeatureExtractor, lock):
    def read_non_ts(data_path, mask_path):

        # opencv image
        if is_image(data_path):
            try:
                img = sitk.ReadImage(data_path, sitk.sitkInt8)
            except Exception as e:
                logger.info(f"Exception: {e}")
                logger.info(f"Failed to read image using sitk: {data_path}.")
                logger.info(f"Try to read the image using opencv.")
                img = cv_img2sitk_image(data_path)

        # numpy ndarray
        elif is_ndarray(data_path):
            arr = np.load(data_path)
            img = sitk.GetImageFromArray(arr)

        # dicom folder
        elif is_dicom_folder(data_path):
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_img_path = \
                    os.path.join(tmpdir, f"{string.ascii_lowercase}.nii.gz")
                dicom2nifti.dicom_series_to_nifti(data_path, tmp_img_path)
                img = sitk.ReadImage(tmp_img_path)

        # try to read image using SimpleITK
        else:
            img = sitk.ReadImage(data_path)

        mask = get_mask(mask_path=mask_path,
                        shape=(img.GetHeight(), img.GetWidth()))

        # to avoiding ITK ERROR:
        # LabelStatisticsImageFilter(0x1263e0bb0): inputs do not occupy
        # the same physical space!
        mask.SetOrigin(img.GetOrigin())
        mask.SetSpacing(img.GetSpacing())
        mask.SetDirection(img.GetDirection())

        return img, mask

    feature_list: List[OrderedDict] = [
        extractor.execute(*read_non_ts(data, mask))
        for data, mask in zip(data_paths, mask_paths)
    ]

    feature_df = pd.DataFrame(feature_list)
    columns = feature_df.columns.tolist()
    if data_ids:
        feature_df[COL_ID] = data_ids
        feature_df = feature_df[[COL_ID] + columns]
    else:
        feature_df = feature_df[columns]

    feature_df[COL_INDEX] = data_idxs
    feature_df.set_index(COL_INDEX)

    with lock:
        if not os.path.exists(result_labels_path):
            feature_df.to_csv(result_labels_path,
                              index=True,
                              index_label=COL_INDEX)
        else:
            feature_df.to_csv(result_labels_path,
                              index=True,
                              mode="a",
                              header=False)


def extract_ts(data_idx: int,
               data_path: str,
               mask_path: str,
               result_dir: str,
               result_path: str,
               extractor: RadiomicsFeatureExtractor,
               original_labels_path: str,
               result_labels_path: str,
               lock):
    def read_ts():
        mask = None
        for frame in iio.imiter(data_path):
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            img = sitk.GetImageFromArray(gray)
            if mask is None:
                mask = get_mask(mask_path=mask_path,
                                shape=(img.GetHeight(), img.GetWidth()))

            yield img, mask

    try:
        feature_list: List[OrderedDict] = \
            [extractor.execute(data, mask) for data, mask in read_ts()]
        feature_df = pd.DataFrame(feature_list)

        if os.path.exists(result_path):
            result_path = rename_duplicate_path(result_path)

        feature_df.to_csv(result_path, index=False)

        with lock:
            if not os.path.exists(result_labels_path):
                result_labels_df = pd.read_csv(original_labels_path)
                for col in [COL_ID, COL_DATA_PATH, COL_MASK_PATH]:
                    if col in result_labels_df:
                        result_labels_df.pop(col)
                result_labels_df[COL_DATA_PATH] = None
                result_labels_df[COL_INDEX] = list(range(result_labels_df.shape[0]))
                result_labels_df.set_index(COL_INDEX)
            else:
                result_labels_df = pd.read_csv(result_labels_path,
                                               index_col=COL_INDEX)

            rel_path = os.path.relpath(result_path, result_dir)
            result_labels_df.loc[data_idx, COL_DATA_PATH] = rel_path

            pop_unnamed(result_labels_df).to_csv(result_labels_path,
                                                 index=True,
                                                 index_label=COL_INDEX)

    except Exception as e:
        logger.warning(traceback.format_exc())
        logger.warning(f"Radiomics extracting error, data_path: {data_path}")


def extract(dataset_dir: str, result_dir: str, config: Union[str, dict],
            processes: int = 2, progress=None) -> RadiomicsFeatureExtractor:
    """

    Parameters
    ----------
    dataset_dir : str
        Directory of the raw dataset.

    result_dir : str
        Directory to save the feature files.

    config : str or dict
        radiomics config of file(yaml or json) path or dict variable.

    processes : int
        Processes to extracting radiomics features.

    """

    dataset = LabeledDataset(root_dir=dataset_dir)

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    else:
        result_file_list = [_ for _ in os.listdir(result_dir)
                            if not _.startswith(".") and not _.startswith("__")]
        if len(result_file_list) > 0:
            file_list_string = '\n- '.join([""] + result_file_list)
            logger.error(f"The result dir '{result_dir}' is not empty with files:{file_list_string}")
            logger.info("Please remove these files and try again!")
            return

    result_labels_path = os.path.join(result_dir, FILENAME_ANNOTATION)

    pool = Pool(processes=processes)
    extractor = RadiomicsFeatureExtractor(config)
    # force to output without additional info
    extractor.settings["additionalInfo"] = False

    data_type = DatasetType.TS if is_video(dataset[0][2]) else DatasetType.NON_TS

    lock = Manager().Lock()

    # non-time series
    if data_type == DatasetType.NON_TS:

        idxs = list(range(len(dataset)))
        group_idxs = [idxs[i: i + GROUP_LEN]
                      for i in range(0, len(idxs), GROUP_LEN)]
        group_data_idxs = [dataset.data_idxs[i: i + GROUP_LEN]
                           for i in range(0, len(idxs), GROUP_LEN)]

        for data_idxs, idx_list in tqdm.tqdm(list(zip(group_data_idxs, group_idxs))):
            extract_non_ts(data_idxs,
                           [dataset.data_ids[_] for _ in idx_list]
                           if dataset.data_ids else None,
                           [dataset.data_paths[_] for _ in idx_list],
                           [dataset.mask_paths[_] for _ in idx_list],
                           result_labels_path,
                           extractor,
                           lock)

        # concat original labels.csv and feature labels.csv
        labels_df = pd.read_csv(dataset.labels_file)
        labels_df[COL_INDEX] = list(range(labels_df.shape[0]))
        labels_df.set_index(COL_INDEX)
        labels_cols = labels_df.columns.tolist()

        feature_df = pd.read_csv(result_labels_path)
        feature_df.set_index(COL_INDEX)
        any_feature_col = [col for col in feature_df.columns
                           if col not in [COL_ID, COL_DATA_PATH, COL_MASK_PATH,
                                          COL_INDEX, COL_LABEL]][0]

        df = pd.concat([labels_df, feature_df], axis=1)
        for col in [COL_ID, COL_MASK_PATH] + \
                   [col for col in df.columns if col.startswith(COL_INDEX)]:
            if col in df:
                df.pop(col)

        # labels.csv
        dff = df[~df[any_feature_col].isna()]
        labels_cols = [col for col in dff.columns if col in labels_cols]
        if COL_LABEL in dff:
            labels_cols = [COL_DATA_PATH, COL_LABEL] + \
                          [col for col in labels_cols if col != COL_DATA_PATH
                           and col != COL_LABEL]
        else:
            labels_cols = [COL_DATA_PATH] + \
                          [col for col in labels_cols if col != COL_DATA_PATH]
        dff[labels_cols].to_csv(result_labels_path, index=False)

        # radiomics data
        result_features_path = os.path.join(result_dir,
                                            RADIOMIC_FEATURE_FILENAME)
        dff.pop(COL_DATA_PATH)
        if COL_LABEL in dff:
            dff.pop(COL_LABEL)
        feature_cols = [col for col in dff.columns if col not in labels_cols]
        dff[feature_cols].to_csv(result_features_path, index=False)

    # time series
    else:  # data_type == 1
        result_paths = [
            os.path.join(result_dir,
                         os.path.splitext(os.path.basename(path))[0] + ".csv")
            for path in dataset.data_paths]

        bar = tqdm.tqdm(total=len(dataset))
        if progress is None:
            callback = lambda _: bar.update()
        else:
            progress.set_tqdm(bar=bar)
            callback = progress.update

        for i in range(len(dataset)):
            data_idx, data_id, data_path, mask_path, label = dataset[i]
            result_path = result_paths[i]
            # extract_ts(data_idx, data_path, mask_path, result_dir,
            #            result_path, extractor, dataset.labels_file,
            #            result_labels_path, lock)
            pool.apply_async(
                func=extract_ts,
                args=(data_idx, data_path, mask_path, result_dir,
                      result_path, extractor, dataset.labels_file,
                      result_labels_path, lock),
                callback=callback
            )

        pool.close()
        pool.join()

        # remove index col and nan data_paths
        df = pd.read_csv(result_labels_path, index_col=COL_INDEX)
        df = df[~df[COL_DATA_PATH].isna()]
        columns = [COL_DATA_PATH] + \
                  [_ for _ in df.columns if _ != COL_DATA_PATH and
                   not _.startswith(COL_INDEX)]
        df[columns].to_csv(result_labels_path, index=False)

    return extractor


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dataset_dir",
        type=str,
        help="raw data dir"
    )
    parser.add_argument(
        "--result_dir",
        type=str,
        help="Directory to save the features result."
    )
    parser.add_argument(
        "--config",
        type=str,
        help="yaml or json file path, or base64 string of json file."
    )
    parser.add_argument(
        "--processes",
        type=int,
        default=2,
        help="multiprocessing pool max size."
    )

    args = parser.parse_args()

    config = args.config
    if isBase64(config):
        config = json.loads(
            base64.decodebytes(config.encode('utf-8')).decode('utf-8'))
    else:
        assert os.path.exists(config), f"config file not exists: {config}"

    logger.info(f"config: {config}")

    extract(dataset_dir=args.dataset_dir,
            config=config,
            result_dir=args.result_dir,
            processes=args.processes)
