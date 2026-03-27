# Copilot Instructions for SUS Brazilian Healthcare Data Processor

## Project Overview

This repository contains a data processing system for Brazilian Healthcare (SUS/DATASUS) data. It processes patient admission records, procedures, costs, and generates statistical reports. The project includes both an original (unoptimized) implementation and an optimized version for performance comparison.

## Tech Stack

- **Language**: Python 3
- **Core library**: pandas (>=2.0.0) — used for all data manipulation
- **Testing**: pytest (>=7.0.0)
- **Data format**: CSV input, JSON export

## Repository Structure

- `healthcare_processor.py` — Original implementation (intentionally unoptimized; do not optimize this file)
- `healthcare_processor_optimized.py` — Optimized implementation using vectorized pandas operations
- `generate_data.py` — Generates sample DATASUS-style CSV data for testing
- `test_processors.py` — Pytest test suite comparing both implementations
- `benchmark.py` — Performance benchmark comparing both implementations
- `requirements.txt` — Python dependencies

## Development Guidelines

### Performance — always prefer vectorized pandas operations

When working on `healthcare_processor_optimized.py` or any new processing code:

- **Never use `iterrows()`** — use vectorized operations, `groupby`, boolean indexing, or `apply` instead
- **Never use bubble sort or manual Python sorting** — use `sort_values()`, `nlargest()`, or `nsmallest()`
- **Never append to a DataFrame in a loop** — use boolean indexing or `pd.concat` on a pre-built list
- **Never do O(n²) duplicate detection** — use `groupby` or `duplicated()`
- **Always index DataFrames** for repeated lookups (e.g., `set_index('patient_id')`)
- Use `pd.to_datetime` once on a column rather than inside a loop
- Use `to_json()` / `read_json()` for JSON export/import rather than row-by-row conversion

### Data Conventions

- Patient IDs are strings in the format `P####` (e.g., `P1042`)
- Dates are strings in `YYYY-MM-DD` format in CSV; convert with `pd.to_datetime` when needed
- Municipality codes are 7-digit IBGE codes (e.g., `3550308` for São Paulo)
- Diagnosis codes follow ICD-10 format (e.g., `U07.1`, `I10`)
- Procedure costs are floats (BRL)

### Adding New Features

- Add new methods to `OptimizedHealthcareDataProcessor` in `healthcare_processor_optimized.py`
- Do **not** modify `healthcare_processor.py` — it serves as the baseline reference
- Mirror any new public API in both classes only if a performance comparison test is needed
- Write tests in `test_processors.py` following the existing class-per-feature pattern

## Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Generate sample data (optional, tests use tmp fixtures)
python generate_data.py

# Run all tests
python -m pytest test_processors.py -v

# Run a specific test class
python -m pytest test_processors.py::TestCostCalculations -v
```

## Running Benchmarks

```bash
python benchmark.py
```

## Key Design Constraints

- The `HealthcareDataProcessor` (original) class must remain unchanged — tests use it as the correctness baseline
- All optimized methods must produce results equivalent to the original (verified by the test suite)
- Float comparisons in tests use `pytest.approx(value, rel=1e-5)` — follow this pattern for any new numeric assertions
