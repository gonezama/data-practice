# Load .env file if it exists
ifneq ("$(wildcard .env)", "")
	include .env
	export
endif

run-ingest:
	python -m ingestion.pipeline $(foreach v,$(MAKEFLAGS),$(if $(findstring =,$(v)),--$(subst =, ,$(v))))
