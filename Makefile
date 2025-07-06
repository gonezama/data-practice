# Load .env file if it exists
ifneq ("$(wildcard .env)", "")
	include .env
	export
endif

# Allow override from command line or use from .env
# START_DATE ?= $(START_DATE)
# END_DATE ?= $(END_DATE)
# DATETIME_COL ?= $(DATETIME_COL)
# DT_FORMAT ?= $(DT_FORMAT)
# DOWNLOAD_OUTPUT_DIR ?= $(DOWNLOAD_OUTPUT_DIR)
# CSV_OUTPUT_DIR ?= $(CSV_OUTPUT_DIR)
# PARQUET_OUTPUT_DIR ?= $(PARQUET_OUTPUT_DIR)

run-ingest:
	python -m ingestion.pipeline $(foreach v,$(MAKEFLAGS),$(if $(findstring =,$(v)),--$(subst =, ,$(v))))
