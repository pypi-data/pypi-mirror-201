import os
import base64
import SimpleITK as sitk

from typing import List, Tuple
from raymics.constants import IMAGE_EXTS, VIDEO_EXTS


def is_hidden(file_path: str) -> bool:
    components = os.path.normpath(file_path).split(os.sep)
    for c in components:
        if c.startswith("."):
            return True
    return False


def is_cacahed(file_path: str) -> bool:
    components = os.path.normpath(file_path).split(os.sep)
    for c in components:
        if c and c.startswith("__"):  # __pycache__, __pypackages__, __MACOSX
            return True
    return False


def get_all_files(root_dir: str) -> List[str]:
    files = []
    for name in os.listdir(root_dir):
        abs_path = os.path.join(root_dir, name)
        if is_hidden(abs_path) or is_cacahed(abs_path):
            continue
        if os.path.isdir(abs_path):
            files += get_all_files(abs_path)
        else:
            files.append(abs_path)
    return files


def is_video(path: str) -> bool:
    ext = os.path.splitext(path)[1].replace(".", "")
    if not ext:
        return False
    else:
        return ext.lower() in VIDEO_EXTS


def is_image(path: str) -> bool:
    ext = os.path.splitext(path)[1].replace(".", "")
    if not ext:
        return False
    else:
        return ext.lower() in IMAGE_EXTS


def is_ndarray(path: str) -> bool:
    ext = os.path.splitext(path)[1].replace(".", "")
    if not ext:
        return False
    else:
        return ext.lower() == "npy"


def is_labelme(path: str) -> bool:
    ext = os.path.splitext(path)[1].replace(".", "")
    if not ext:
        return False
    else:
        return ext.lower() == "json"


def is_dicom_folder(path: str) -> bool:
    if not os.path.isdir(path):
        return False
    else:
        dicom_paths = [p for p in get_all_files(path)
                       if p.lower().endswith(".dcm")]
        if dicom_paths:
            return True
        else:
            return False


def get_sitk_shape(image: sitk.Image) -> Tuple[int, int, int]:
    """Get the shape of SimpleITK image shape"""
    return image.GetWidth(), image.GetHeight(), image.GetDepth()


def isBase64(s):
    try:
        if isinstance(s, str):
            s_bytes = bytes(s, 'ascii')
        elif isinstance(s, bytes):
            s_bytes = s
        else:
            raise ValueError("Argument must be string or bytes")
        return base64.b64encode(base64.b64decode(s_bytes)) == s_bytes
    except Exception:
        return False
