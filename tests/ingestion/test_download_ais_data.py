import os
import pytest
from unittest import mock
from ingestion.download_ais_data import download_ais_data, download_zip

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


@pytest.fixture
def mock_check_if_date_is_already_processed():
    with mock.patch(
        "ingestion.download_ais_data.check_if_date_is_already_processed",
        return_value=False,
    ):
        yield


def test_download_ais_data(
    mock_requests_get,
    mock_open_write,
    mock_os_path_exists,
    mock_os_makedirs,
    mock_check_if_date_is_already_processed,
):
    # Mock base page with links
    mock_response = mock.Mock()
    mock_response.text = HTML_SAMPLE
    mock_response.raise_for_status = mock.Mock()
    mock_requests_get.return_value = mock_response

    # Mock zip download responses
    zip_response = mock.Mock()
    zip_response.iter_content = lambda chunk_size: [b"test-data"]
    zip_response.raise_for_status = mock.Mock()
    mock_requests_get.side_effect = [
        mock_response,
        zip_response,
        zip_response,
        zip_response,
    ]  # 1 HTML + 3 ZIPs

    results = list(
        download_ais_data(
            start_date="2024-01-01",
            end_date="2024-03-02",
            output_dir="test_dir",
        )
    )

    assert len(results) == 3
    for path in results:
        assert path.startswith("test_dir/aisdk-2024")

    assert mock_requests_get.call_count == 4
    mock_open_write.assert_called()
    mock_os_makedirs.assert_called_with("test_dir", exist_ok=True)


def test_download_zip_skips_existing_file():
    with mock.patch("os.path.exists", return_value=True):
        with mock.patch("ingestion.download_ais_data.logger") as mock_logger:
            with mock.patch("ingestion.download_ais_data.requests.get") as mock_get:
                result = download_zip("http://example.com/aisdk-2024-01.zip", "test_dir")
                assert result == "test_dir/aisdk-2024-01.zip"
                mock_get.assert_not_called()
                mock_logger.info.assert_called_with(
                    "File already exists, skipping download: test_dir/aisdk-2024-01.zip"
                )
