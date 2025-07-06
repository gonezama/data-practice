import os
from loguru import logger

from ingestion.download_ais_data import download_ais_data
from ingestion.extract_zip_contents import extract_zip
from utils.get_filespaths_in_folder import list_files_by_extension
from utils.tree_clean_up import delete_folder
from ingestion.extract_zip_contents import extract_zip
from ingestion.t_into_parquet import lazy_csv_to_parquet


def main_pipeline(download_output_dir, csv_output_dir, parquet_output_dir):

    logger.info("Starting ingestion pipeline")

    for f_path in download_ais_data(
        start_date="2024-10-10", end_date="2024-10-10", output_dir=download_output_dir
    ):
        for extracted_csv in extract_zip(f_path, csv_output_dir):
            lazy_csv_to_parquet(
                extracted_csv,
                output_path=parquet_output_dir,
                datetime_col="# Timestamp",
                dt_format="%d/%m/%Y %H:%M:%S",
            )

    delete_folder(download_output_dir)
    delete_folder(csv_output_dir)
    logger.info("Finished ingestion pipeline")


if __name__ == "__main__":

    download_output_dir = "./ais_downloaded_data"
    csv_output_dir = "./ais_csv_data"
    parquet_output_dir = "./ais_data"

    main_pipeline(
        download_output_dir=download_output_dir,
        csv_output_dir=csv_output_dir,
        parquet_output_dir=parquet_output_dir,
    )
