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

Data is sourced: "https://www.bcra.gob.ar/Pdfs/PublicacionesEstadisticas/historico-relevamiento-expectativas-mercado.xlsx"

# Project Structure

`ingestion/`: Scripts to download, extract, and save into duckdb database.

# Ingestion

## Run Ingest:
```bash
make run-ingest
```

## Notes

Had to change source since other source (Denmark AIS data) was shutdown.