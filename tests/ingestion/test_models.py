from ingestion.models import IngestJobParameters


def test_ingengest_job_parameters_defaults():
    params = IngestJobParameters()
    assert params.start_date == "2024-10-10"
    assert params.end_date == "2024-10-11"
    assert params.datetime_col == "# Timestamp"
    assert params.dt_format == "%d/%m/%Y %H:%M:%S"
    assert params.download_output_dir == "./ais_downloaded_data"
    assert params.csv_output_dir == "./ais_csv_data"
    assert params.parquet_output_dir == "./ais_data"


def test_ingengest_job_parameters_custom_values():
    custom_params = IngestJobParameters(
        start_date="2023-01-01",
        end_date="2023-01-31",
        datetime_col="timestamp",
        dt_format="%Y-%m-%d %H:%M:%S",
        download_output_dir="/tmp/downloads",
        csv_output_dir="/tmp/csv",
        parquet_output_dir="/tmp/parquet",
    )
    assert custom_params.start_date == "2023-01-01"
    assert custom_params.end_date == "2023-01-31"
    assert custom_params.datetime_col == "timestamp"
    assert custom_params.dt_format == "%Y-%m-%d %H:%M:%S"
    assert custom_params.download_output_dir == "/tmp/downloads"
    assert custom_params.csv_output_dir == "/tmp/csv"
    assert custom_params.parquet_output_dir == "/tmp/parquet"
