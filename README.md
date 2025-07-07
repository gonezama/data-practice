# data-practice

A data engineering practice project with toy data, inspired by [this data engineering project video](https://www.youtube.com/watch?v=3pLKTmdWDXk&t=1s). The video demonstrates many good practices and procedures, though this repo adapts and changes some elements in order to experiment with other tools.

## Requirements

- Python 3.12.11
- See `requirements.txt` for package dependencies:
    - loguru
    - requests
    - beautifulsoup4
    - fire
    - pydantic
    - polars

Install dependencies with:
```bash
pip install -r requirements.txt
```

# Data Source

Data is sourced from: https://web.ais.dk/aisdata/

# Project Structure

`ingestion/`: Scripts to download, extract, and process AIS data.
`utils/`: Utility scripts (e.g., file path helpers).
`tests/`: Pytest-based tests for ingestion logic.


## ToDos
[] Build a lazyframe validation to deal with unconventional columns names
