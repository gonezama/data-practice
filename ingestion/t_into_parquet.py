import polars as pl
from polars.io.partition import PartitionByKey


def partitioning(datetime_col, output_path):
    return PartitionByKey(
        output_path,
        by=[
            pl.col(datetime_col).dt.year().alias('Year'),
            pl.col(datetime_col).dt.month().alias('Month'),
            pl.col(datetime_col).dt.day().alias('Day'),
            pl.col(datetime_col).dt.hour().alias('Hour'),
        ],
        per_partition_sort_by=pl.col(datetime_col),
        include_key=True,  # typically you don't need the date col inside each file
        file_path=lambda ctx: f"{ctx.keys[0].str_value}/{ctx.keys[1].str_value}/{ctx.keys[2].str_value}/part-hour-{ctx.keys[3].str_value}.parquet",
    )


def lazy_csv_to_parquet(
    filepath,
    output_path="./ais_data",
    datetime_col="# Timestamp",
    dt_format="%d/%m/%Y %H:%M:%S",
):
    pl.scan_csv(filepath).with_columns(
        pl.col(datetime_col).str.strptime(pl.Datetime, format=dt_format)
    ).unique().sink_parquet(partitioning(datetime_col, output_path), mkdir=True)
