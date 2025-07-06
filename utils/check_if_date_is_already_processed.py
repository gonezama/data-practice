import os
from datetime import datetime
import polars as pl

def check_if_date_is_already_processed(
    date_str: str,
    output_path: str,
) -> bool:
    """
    Check if a given date (YYYY-MM-DD) is already processed in the partitioned Parquet output.

    Args:
        date_str (str): Date string in "YYYY-MM-DD" format.
        output_path (str): Root path where partitioned Parquet files are stored.

    Returns:
        bool: True if the date is already processed, False otherwise.
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("date_str must be in 'YYYY-MM-DD' format")

    year = str(date_obj.year)
    month = f"{date_obj.month:02d}"
    day = f"{date_obj.day:02d}"

    day_path = os.path.join(output_path, year, month, day)

    if not os.path.exists(day_path):
        return False
    # Just check if the folder has any parquet files
    for file in os.listdir(day_path):
        if file.endswith(".parquet"):
            return True
    return False