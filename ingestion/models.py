from pydantic import BaseModel

class IngestJobParameters(BaseModel):
    start_date: str = "2024-10-10"
    end_date: str = "2024-10-11"
    datetime_col: str  = "# Timestamp"
    dt_format:str = "%d/%m/%Y %H:%M:%S"
    download_output_dir: str = "./ais_downloaded_data"
    csv_output_dir: str = "./ais_csv_data"
    parquet_output_dir: str = "./ais_data"

