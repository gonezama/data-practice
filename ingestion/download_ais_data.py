import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from loguru import logger

import os
import re
from datetime import datetime

from utils.check_if_date_is_already_processed import check_if_date_is_already_processed

def download_ais_data(
    start_date: str = None,
    end_date: str = None,
    output_dir: str = "ais_downloaded_data",
):
    """
    Generator that yields paths to downloaded AIS zip files
    from the Danish Maritime Authority.

    Parameters:
        start_date (str): Start date in 'YYYY-MM-DD' format (inclusive)
        end_date (str): End date in 'YYYY-MM-DD' format (inclusive)
        output_dir (str): Directory where the zip files and contents will be saved
    Yields:
        str: Local path to each downloaded ZIP file
    """
    BASE_URL = "https://web.ais.dk/aisdata/"
    response = requests.get(BASE_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    os.makedirs(output_dir, exist_ok=True)

    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    except ValueError:
        raise ValueError("Dates must be in 'YYYY-MM-DD' format.")

    daily_cutoff = datetime.strptime("2024-03-01", "%Y-%m-%d")
    logger.info(f"Fetching data from {start_date} to {end_date}")

    for a in soup.find_all("a", href=True):
        href = a["href"]

        # Monthly files
        monthly_match = re.match(r"aisdk-(\d{4})-(\d{2})\.zip", href)
        if monthly_match:
            year, month = monthly_match.groups()
            file_date = datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d")
            if file_date < daily_cutoff:
                if (start_dt is None or file_date >= start_dt) and (
                    end_dt is None or file_date <= end_dt
                ):
                    if check_if_date_is_already_processed(date_str=file_date.strftime("%Y-%m-%d"), output_path='ais_data'):
                        logger.info(f"{file_date.strftime("%Y-%m-%d")} data is already available as parquet")
                        continue
                    url = urljoin(BASE_URL, href)
                    logger.info(f"Downloading monthly file: {url}")
                    output_path = download_zip(url, output_dir)
                    if output_path:
                        yield output_path
            continue

        # Daily files
        daily_match = re.match(r"aisdk-(\d{4})-(\d{2})-(\d{2})\.zip", href)
        if daily_match:
            year, month, day = daily_match.groups()
            file_date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
            if file_date >= daily_cutoff:
                if (start_dt is None or file_date >= start_dt) and (
                    end_dt is None or file_date <= end_dt
                ):
                    if check_if_date_is_already_processed(date_str=file_date.strftime("%Y-%m-%d"), output_path='ais_data'):
                        logger.info(f"{file_date.strftime("%Y-%m-%d")} data is already available as parquet")
                        continue

                    url = urljoin(BASE_URL, href)
                    logger.info(f"Downloading daily file: {url}")
                    output_path = download_zip(url, output_dir)
                    if output_path:
                        yield output_path


def download_zip(url: str, output_dir: str) -> str:
    """
    Downloads a zip file from the given URL and saves it to the specified directory.

    Parameters:
        url (str): The URL of the zip file
        output_dir (str): Directory where the file will be saved

    Returns:
        str: Full local path to the saved zip file
    """
    local_zip_path = os.path.join(output_dir, os.path.basename(url))

    # Skip download if file already exists
    if os.path.exists(local_zip_path):
        logger.info(f"File already exists, skipping download: {local_zip_path}")
        return local_zip_path

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to download {url}: {e}")
        return None

    try:
        with open(local_zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive chunks
                    f.write(chunk)
        logger.info(f"Downloaded and saved: {local_zip_path}")
        return local_zip_path
    except IOError as e:
        logger.error(f"Failed to write file {local_zip_path}: {e}")
        return None


def download_ais_data_batch(
    start_date: str = None,
    end_date: str = None,
    output_dir: str = "ais_downloaded_data",
):
    return list(
        download_ais_data(
            start_date=start_date, end_date=end_date, output_dir=output_dir
        )
    )
