import os
import pytest
from unittest import mock
from ingestion.download_ais_data import download_ais_data, download_zip

from io import BytesIO

# Sample HTML listing AIS files
HTML_SAMPLE = """
<html><body>
<a href="aisdk-2024-01.zip">aisdk-2024-01.zip</a>
<a href="aisdk-2024-03-01.zip">aisdk-2024-03-01.zip</a>
<a href="aisdk-2024-03-02.zip">aisdk-2024-03-02.zip</a>
</body></html>
"""


@pytest.fixture
def mock_requests_get():
    with mock.patch("ingestion.download_ais_data.requests.get") as mock_get:
        yield mock_get


@pytest.fixture
def mock_open_write():
    with mock.patch("builtins.open", mock.mock_open()) as mock_file:
        yield mock_file


@pytest.fixture
def mock_os_path_exists():
    with mock.patch("os.path.exists", return_value=False):
        yield


@pytest.fixture
def mock_os_makedirs():
    with mock.patch("os.makedirs") as mock_mkdirs:
        yield mock_mkdirs


def test_download_ais_data(
    mock_requests_get, mock_open_write, mock_os_path_exists, mock_os_makedirs
):
    # Mock base page with links
    mock_response = mock.Mock()
    mock_response.text = HTML_SAMPLE
    mock_response.raise_for_status = mock.Mock()
    mock_requests_get.return_value = mock_response

    # Mock zip download
    zip_response = mock.Mock()
    zip_response.iter_content = lambda chunk_size: [b"data"]
    zip_response.raise_for_status = mock.Mock()
    mock_requests_get.side_effect = [
        mock_response,
        zip_response,
        zip_response,
        zip_response,
    ]  # once for HTML, twice for zip files

    output = download_ais_data(
        start_date="2024-01-01", end_date="2024-03-02", output_dir="test_dir"
    )

    assert output == "test_dir"
    assert mock_requests_get.call_count == 4  # 1 HTML + 3 zip downloads
    mock_open_write.assert_called()  # zip files were written
    mock_os_makedirs.assert_called_with("test_dir", exist_ok=True)


def test_download_zip_skips_existing_file():
    with mock.patch("os.path.exists", return_value=True):  # <- this is the fix
        with mock.patch("ingestion.download_ais_data.logger") as mock_logger:
            with mock.patch("ingestion.download_ais_data.requests.get") as mock_get:
                download_zip("http://example.com/aisdk-2024-01.zip", "test_dir")
                mock_get.assert_not_called()
                mock_logger.info.assert_called_with(
                    "File already exists: test_dir/aisdk-2024-01.zip"
                )
