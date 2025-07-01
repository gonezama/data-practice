from ingestion.download_ais_data import download_ais_data

files = download_ais_data("2024-10-28", "2024-10-29")

import polars as pl
from zipfile import ZipFile


zip_file = "ais_data/aisdk-2024-10-29.zip"
csv_name = "aisdk-2024-10-29.csv"
a = pl.read_csv("ais_data/aisdk-2024-10-29.csv", n_rows=20)
a

a = pl.read_csv(ZipFile(zip_file).read(csv_name))
a
