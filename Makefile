# Load .env file if it exists
ifneq ("$(wildcard .env)", "")
	include .env
	export
endif

# Allow override from command line or use from .env
START_DATE ?= $(START_DATE)
END_DATE ?= $(END_DATE)
DATETIME_COL ?= $(DATETIME_COL)
DT_FORMAT ?= $(DT_FORMAT)
DOWNLOAD_OUTPUT_DIR ?= $(DOWNLOAD_OUTPUT_DIR)
CSV_OUTPUT_DIR ?= $(CSV_OUTPUT_DIR)
PARQUET_OUTPUT_DIR ?= $(PARQUET_OUTPUT_DIR)

run-ingest:
	python -m ingestion.pipeline \
		--start_date=$(START_DATE) \
		--end_date=$(END_DATE) \
		--datetime_col="$(DATETIME_COL)" \
		--dt_format="$(DT_FORMAT)" \
		--download_output_dir=$(DOWNLOAD_OUTPUT_DIR) \
		--csv_output_dir=$(CSV_OUTPUT_DIR) \
		--parquet_output_dir=$(PARQUET_OUTPUT_DIR)
