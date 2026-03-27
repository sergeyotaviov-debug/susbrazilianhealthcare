# GitHub Copilot Instructions for SUS Brazilian Healthcare Data Processor

## Project Overview

This repository contains a high-performance data processing system for Brazilian Healthcare (SUS/DATASUS) data. The project focuses on efficiently processing patient admission data, procedures, costs, and generating various analytical reports.

**Primary Goal:** Process large-scale healthcare datasets with optimal performance while maintaining code clarity and correctness.

## Tech Stack

- **Language:** Python 3.x
- **Primary Library:** pandas >= 2.0.0
- **Testing Framework:** pytest >= 7.0.0
- **Data Format:** CSV input files, JSON export capability
- **Architecture:** Object-oriented with performance-optimized implementations

## Coding Guidelines

### Performance First

This project prioritizes performance optimization for large-scale data processing:

1. **Always use vectorized operations** instead of row-by-row iteration (no `iterrows()`)
2. **Leverage pandas built-in methods** like `groupby()`, `nlargest()`, `nunique()`, `merge()`
3. **Use boolean indexing** for filtering instead of loops or `append()`
4. **Single-pass processing:** Filter once, calculate multiple metrics from filtered data
5. **Create indices** for frequently searched columns (O(1) lookups vs O(n))

### Python Style Conventions

- **Type hints:** Use type hints for function signatures (see existing code for examples)
- **Docstrings:** Include clear docstrings explaining:
  - What the method does
  - Any optimization strategy applied
  - Performance characteristics (e.g., "O(n) instead of O(n²)")
- **Naming:** Use descriptive snake_case for functions and variables
- **Class structure:** Maintain instance variables for data caching and indexing

### Code Patterns to Follow

#### ✅ GOOD - Vectorized Operations
```python
def calculate_total_cost_per_patient(self) -> Dict[str, float]:
    """Uses groupby for efficient aggregation - O(n)"""
    patient_costs = self.data.groupby('patient_id')['procedure_cost'].sum()
    return patient_costs.to_dict()
```

#### ❌ AVOID - Row Iteration
```python
def calculate_total_cost_per_patient(self) -> Dict[str, float]:
    patient_costs = {}
    for index, row in self.data.iterrows():  # 100x slower!
        # ... processing logic
    return patient_costs
```

#### ✅ GOOD - Boolean Indexing
```python
def filter_by_municipality(self, municipality_code: str) -> pd.DataFrame:
    """Single vectorized operation - O(n)"""
    return self.data[self.data['municipality_code'] == municipality_code].copy()
```

#### ❌ AVOID - DataFrame Append in Loop
```python
def filter_by_municipality(self, municipality_code: str):
    filtered_data = pd.DataFrame()
    for index, row in self.data.iterrows():
        if row['municipality_code'] == municipality_code:
            filtered_data = filtered_data.append(row)  # O(n²) - creates copies!
    return filtered_data
```

#### ✅ GOOD - Built-in Sorting
```python
def get_top_expensive_procedures(self, n: int = 10) -> List[Dict]:
    """Uses nlargest() - O(n log n)"""
    top_procedures = self.data.nlargest(n, 'procedure_cost')[...].to_dict('records')
    return top_procedures
```

#### ❌ AVOID - Manual Sorting
```python
def get_top_expensive_procedures(self, n: int = 10):
    # Bubble sort - O(n²) - 1000x slower for large datasets!
    for i in range(len(procedures)):
        for j in range(len(procedures) - 1 - i):
            # ... swap logic
```

## Project Structure

```
.
├── healthcare_processor.py          # Original implementation (baseline)
├── healthcare_processor_optimized.py # Performance-optimized version
├── test_processors.py               # Unit tests for both implementations
├── benchmark.py                     # Performance benchmarks
├── generate_data.py                 # Test data generation
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
├── OPTIMIZATIONS.md                 # Detailed optimization guide
└── SUMMARY.md                       # Performance summary
```

## Key Data Schema

Healthcare records contain the following fields:
- `patient_id`: Unique patient identifier
- `procedure_name`: Name of medical procedure
- `procedure_cost`: Cost in BRL (Brazilian Real)
- `diagnosis_code`: Medical diagnosis code
- `municipality_code`: Municipality identifier
- `admission_date`: Patient admission date (datetime)
- `discharge_date`: Patient discharge date (datetime)

## Testing Guidelines

1. **Functional equivalence:** Optimized implementations must produce identical results to original
2. **Use fixtures:** Leverage pytest fixtures for test data setup (see `test_processors.py`)
3. **Test both implementations:** Verify original and optimized versions produce same results
4. **Approximate comparisons:** Use `pytest.approx()` for floating-point comparisons
5. **Cover edge cases:** Empty datasets, missing values, duplicate records

### Test Execution
```bash
# Run all tests
pytest test_processors.py -v

# Run specific test class
pytest test_processors.py::TestCostCalculations -v

# Run benchmarks
python benchmark.py
```

## Performance Expectations

When suggesting or reviewing code, consider these performance targets:

| Operation | Target Performance | Complexity |
|-----------|-------------------|------------|
| Data loading | < 0.1s per 10K records | O(n) |
| Cost aggregation | < 0.05s per 10K records | O(n) |
| Top N sorting | < 0.05s per 10K records | O(n log n) |
| Filtering | < 0.02s per 10K records | O(n) |
| Patient lookup | < 0.001s with index | O(1) |
| Duplicate detection | < 0.2s per 10K records | O(n) |

## Common Operations Reference

### Data Loading
```python
# Standard loading
processor = OptimizedHealthcareDataProcessor(data_file)
processor.load_data()

# Chunked loading for very large files
for chunk in processor.load_data(chunksize=10000):
    # Process chunk
```

### Filtering and Aggregation
```python
# Use boolean masks
mask = (df['admission_date'].dt.year == year) & (df['admission_date'].dt.month == month)
filtered = df[mask]

# Use groupby for aggregation
patient_totals = df.groupby('patient_id')['cost'].sum()
```

### Working with Dates
```python
# Convert to datetime once during load
df['admission_date'] = pd.to_datetime(df['admission_date'])

# Use dt accessor for operations
df['admission_date'].dt.year
df['admission_date'].dt.month
```

## Security and Data Handling

- **No hardcoded credentials:** Use environment variables or config files
- **Validate input data:** Check for required columns before processing
- **Handle missing data:** Use pandas methods like `dropna()`, `fillna()`
- **File paths:** Use absolute paths or proper path joining
- **Large files:** Support chunked processing to avoid memory issues

## Documentation Standards

When adding new methods, include:

1. **Docstring with:**
   - Clear description of functionality
   - Args and return type documentation
   - Optimization strategy used
   - Performance characteristics

2. **Example:**
```python
def new_analysis_method(self, param: str) -> Dict[str, Any]:
    """
    Analyze data using specific criteria

    Optimization: Uses vectorized pandas operations with groupby
    Performance: O(n) single-pass processing

    Args:
        param: Description of parameter

    Returns:
        Dictionary with analysis results
    """
    # Implementation
```

## Key References

- **Pandas Documentation:** https://pandas.pydata.org/docs/
- **Performance Tips:** See `OPTIMIZATIONS.md` for detailed examples
- **Project README:** See `README.md` for setup and usage

## AI Assistant Guidelines

When generating code for this project:

1. **Prioritize performance:** Always suggest vectorized pandas operations
2. **Match existing patterns:** Follow the style in `healthcare_processor_optimized.py`
3. **Include type hints:** All function signatures should have type annotations
4. **Add optimization notes:** Document performance characteristics in docstrings
5. **Consider scalability:** Code should handle 10K+ records efficiently
6. **Test compatibility:** Ensure new code works with existing test suite
7. **Avoid deprecated pandas methods:** No `append()`, use `concat()` or boolean indexing
8. **Memory efficiency:** Consider chunked processing for large-scale operations

## Common Mistakes to Avoid

1. ❌ Using `iterrows()` or `itertuples()` when vectorization is possible
2. ❌ Creating new DataFrames in loops (quadratic memory behavior)
3. ❌ Manually implementing algorithms that pandas provides (sorting, grouping, etc.)
4. ❌ Multiple iterations when single-pass is possible
5. ❌ Linear search when indexed lookup is available
6. ❌ Converting to Python lists/dicts prematurely (stay in pandas as long as possible)
7. ❌ Using deprecated pandas APIs (check pandas version compatibility)

## Success Criteria

Code contributions should:
- ✅ Pass all existing unit tests
- ✅ Maintain or improve performance benchmarks
- ✅ Follow pandas best practices for vectorization
- ✅ Include appropriate type hints and docstrings
- ✅ Handle edge cases gracefully
- ✅ Be readable and maintainable
