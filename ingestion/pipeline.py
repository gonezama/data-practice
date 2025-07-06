from loguru import logger
from fire import Fire

from ingestion.models import IngestJobParameters
from ingestion.download_ais_data import download_ais_data
from ingestion.extract_zip_contents import extract_zip
from utils.tree_clean_up import delete_folder
from ingestion.extract_zip_contents import extract_zip
from ingestion.t_into_parquet import lazy_csv_to_parquet


def ingest_pipeline(params: IngestJobParameters):

    logger.info("Starting ingestion pipeline")
    for f_path in download_ais_data(
        start_date=params.start_date, end_date=params.end_date, output_dir=params.download_output_dir
    ):
        for extracted_csv in extract_zip(f_path, params.csv_output_dir):
            lazy_csv_to_parquet(
                extracted_csv,
                output_path=params.parquet_output_dir,
                datetime_col=params.datetime_col,
                dt_format=params.dt_format,
            )

    delete_folder(params.download_output_dir)
    delete_folder(params.csv_output_dir)
    logger.info("Finished ingestion pipeline")


if __name__ == "__main__":
    Fire(lambda **kwargs: ingest_pipeline(IngestJobParameters(**kwargs)))