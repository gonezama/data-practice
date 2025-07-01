import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from loguru import logger
import zipfile
import io
import os

# Base URL of the data directory
BASE_URL = "https://web.ais.dk/aisdata/"

# Make request to get HTML listing
response = requests.get(BASE_URL)
response.raise_for_status()  # Ensure we got a valid response

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find all links that end in .zip
zip_links = [
    urljoin(BASE_URL, a["href"])
    for a in soup.find_all("a", href=True)
    if a["href"].endswith(".zip")
]


# # Download and unzip each file
# for link in zip_links:
#     print(f"Downloading {link}")
#     zip_resp = requests.get(link)
#     zip_resp.raise_for_status()

#     # Unzip in memory
#     with zipfile.ZipFile(io.BytesIO(zip_resp.content)) as z:
#         print(f"Extracting {link}")
#         z.extractall("downloaded_aisdata")

# print("All files downloaded and extracted.")
