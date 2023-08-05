import os
import numpy as np
import pandas as pd

from typing import List, Tuple, Union
from raymics.constants import FILENAME_ANNOTATION, COL_DATA_PATH, \
    COL_MASK_PATH, COL_LABEL, COL_ID
from raymics.log import logger


READ_DATA_TYPE = Tuple[List[int],
                       List,
                       List[str],
                       List[Union[str, None]],
                       List[Union[str, int, float]]]
GET_ITEM_TYPE = Tuple[str, Union[str, None], Union[str, int, float]]


class Dataset:

    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def __getitem__(self, idx: int) -> GET_ITEM_TYPE:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError


class LabeledDataset(Dataset):
    """2D or videos dataset annotated with labels.csv."""

    def __init__(self, root_dir: str):
        super().__init__(root_dir)
        self.labels_file = os.path.join(self.root_dir, FILENAME_ANNOTATION)
        assert os.path.exists(self.labels_file), \
            f"Not found labels.csv: {self.labels_file}"
        self.data_idxs, self.data_ids, self.data_paths, self.mask_paths, \
            self.labels = self.read_data()

    def __len__(self):
        return len(self.data_paths)

    def read_data(self) -> READ_DATA_TYPE:
        data_idxs = []
        data_ids = []
        data_paths = []
        mask_paths = []
        labels = []

        labels_file_path = os.path.join(self.root_dir, FILENAME_ANNOTATION)
        if os.path.exists(labels_file_path):
            df = pd.read_csv(labels_file_path)

            logger.info(f"{FILENAME_ANNOTATION} with {df.shape[0]} rows "
                        f"and {df.shape[1]} columns: {', '.join(df.columns)}")

            assert COL_DATA_PATH in df, \
                f"Column '{COL_DATA_PATH}' not found in {FILENAME_ANNOTATION}!"

            if COL_MASK_PATH not in df:
                logger.info(f"{FILENAME_ANNOTATION} has no column {COL_MASK_PATH}")

            has_ids = COL_ID in df
            has_label = COL_LABEL in df
            for i in range(df.shape[0]):
                data_path = os.path.join(self.root_dir,
                                         df[COL_DATA_PATH].iloc[i])
                if not os.path.exists(data_path):
                    logger.warning(
                        f"Ignoring data_{i} cause data_path not exists: {data_path}")
                    continue

                if COL_MASK_PATH not in df:
                    mask_path = None
                else:
                    mask_path = df[COL_MASK_PATH].iloc[i]
                    if isinstance(mask_path, float):
                        if np.isnan(mask_path):
                            mask_path = None
                        else:
                            mask_path = os.path.join(self.root_dir, str(mask_path))
                    else:
                        mask_path = os.path.join(self.root_dir, mask_path)

                    if mask_path is not None and not os.path.exists(mask_path):
                        logger.warning(
                            f"Ignoring data_{i} cause mask_path not exists: {mask_path}")
                        continue

                data_idxs.append(i)
                data_paths.append(data_path)
                mask_paths.append(mask_path)
                if has_ids:
                    data_ids.append(df[COL_ID].iloc[i])
                if has_label:
                    labels.append(df[COL_LABEL].iloc[i])

        if not data_paths:
            logger.error(f"No any valid data found!")

        return data_idxs, data_ids, data_paths, mask_paths, labels

    def __getitem__(self, idx: int):
        return self.data_idxs[idx],\
               self.data_ids[idx] if self.data_ids else None,\
               self.data_paths[idx], \
               self.mask_paths[idx], \
               self.labels[idx] if self.labels else None
