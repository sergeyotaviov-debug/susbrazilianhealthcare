# SUS Brazilian Healthcare Data Processor

This repository contains a data processing system for Brazilian Healthcare (SUS/DATASUS) data.

## Overview

The healthcare processor handles patient admission data, procedures, costs, and generates various reports.

## Identified Performance Issues

### Current Implementation Issues (healthcare_processor.py)

The current implementation has several significant performance problems:

1. **Inefficient Iteration with `iterrows()`** (Multiple methods)
   - Methods like `calculate_total_cost_per_patient()`, `get_procedures_by_diagnosis()`, etc. use `iterrows()`
   - This is extremely slow for large datasets (10-100x slower than vectorized operations)
   - Impact: O(n) operations that could be O(1) with proper pandas operations

2. **Bubble Sort Algorithm** (`get_top_expensive_procedures()`)
   - Uses bubble sort with O(n²) complexity
   - For 10,000 records, this means ~100 million comparisons
   - Should use built-in sorting or pandas methods with O(n log n) complexity

3. **DataFrame Append in Loop** (`filter_by_municipality()`)
   - Uses deprecated `DataFrame.append()` in a loop
   - Creates new DataFrame copy on each iteration
   - Results in O(n²) memory operations

4. **Multiple Data Iterations** (`generate_monthly_report()`)
   - Iterates through entire dataset 3 separate times
   - Each iteration is O(n), resulting in 3n operations
   - Should filter once and calculate all metrics from filtered data

5. **O(n²) Duplicate Detection** (`find_duplicate_procedures()`)
   - Nested loops comparing every record with every other record
   - For 10,000 records: 50 million comparisons
   - Should use groupby or hash-based deduplication

6. **No Data Indexing** (`search_patient_by_id()`)
   - Linear search through all records for every query
   - O(n) lookup when it should be O(1) with proper indexing

7. **Row-by-row JSON Conversion** (`export_to_json()`)
   - Converts each row individually instead of using pandas built-in methods
   - Inefficient memory usage and slow

8. **No Chunking for Large Files** (`load_data()`)
   - Loads entire CSV into memory at once
   - Will fail or be very slow for files larger than available RAM

## Performance Impact Examples

For a dataset with 10,000 records:
- `calculate_total_cost_per_patient()`: ~2-5 seconds (should be <0.1s)
- `get_top_expensive_procedures()`: ~30-60 seconds (should be <0.1s)
- `filter_by_municipality()`: ~5-10 seconds (should be <0.1s)
- `generate_monthly_report()`: ~6-15 seconds (should be <0.2s)

## Recommended Optimizations

1. Replace all `iterrows()` calls with vectorized pandas operations
2. Use pandas built-in `sort_values()` and `nlargest()` methods
3. Use boolean indexing for filtering instead of append
4. Combine multiple iterations into single-pass operations
5. Use `groupby()` for duplicate detection
6. Add DataFrame indexing for fast lookups
7. Use pandas `to_json()` method
8. Implement chunked reading for large files

## Setup

```bash
# Install dependencies
pip install pandas

# Generate sample data
python generate_data.py

# Run tests
python -m pytest tests/
```

## License

MIT License - see LICENSE file
