import zipfile
import os
from loguru import logger


def extract_zip(local_zip_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    
    with zipfile.ZipFile(local_zip_path, "r") as zip_ref:
        zip_ref.extractall(output_dir)
        logger.info(f"Extracted to: {output_dir}")
        for name in zip_ref.namelist():
            full_path = os.path.join(output_dir, name)
            yield full_path


def extract_zip_and_list(local_zip_path: str, output_dir: str):
    return list(extract_zip(local_zip_path=local_zip_path, output_dir=output_dir))
