import shutil
import os
from loguru import logger


def delete_folder(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)
        logger.warning(f"Deleted folder: {path}")
    else:
        logger.warning(f"Folder does not exist: {path}")
