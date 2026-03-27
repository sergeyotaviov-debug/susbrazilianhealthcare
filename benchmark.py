"""
Performance comparison between original and optimized implementations
"""
import time
import pandas as pd
from healthcare_processor import HealthcareDataProcessor
from healthcare_processor_optimized import OptimizedHealthcareDataProcessor
from generate_data import generate_sample_data


def measure_time(func, *args, **kwargs):
    """Measure execution time of a function"""
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return end - start, result


def run_benchmark(data_file='sample_data.csv', num_records=1000):
    """Run performance comparison benchmark"""
    
    print(f"\n{'='*70}")
    print(f"Performance Benchmark - {num_records} records")
    print(f"{'='*70}\n")
    
    # Generate sample data
    print("Generating sample data...")
    generate_sample_data(num_records, data_file)
    
    # Initialize processors
    print("\nInitializing processors...")
    original = HealthcareDataProcessor(data_file)
    optimized = OptimizedHealthcareDataProcessor(data_file)
    
    # Load data
    print("\n1. Loading data...")
    orig_time, _ = measure_time(original.load_data)
    opt_time, _ = measure_time(optimized.load_data)
    print(f"   Original: {orig_time:.4f}s")
    print(f"   Optimized: {opt_time:.4f}s")
    print(f"   Speedup: {orig_time/opt_time:.2f}x")
    
    # Test 1: Calculate total cost per patient
    print("\n2. Calculate total cost per patient...")
    orig_time, orig_result = measure_time(original.calculate_total_cost_per_patient)
    opt_time, opt_result = measure_time(optimized.calculate_total_cost_per_patient)
    print(f"   Original: {orig_time:.4f}s")
    print(f"   Optimized: {opt_time:.4f}s")
    print(f"   Speedup: {orig_time/opt_time:.2f}x")
    
    # Test 2: Get top expensive procedures
    print("\n3. Get top 10 expensive procedures...")
    orig_time, orig_result = measure_time(original.get_top_expensive_procedures, 10)
    opt_time, opt_result = measure_time(optimized.get_top_expensive_procedures, 10)
    print(f"   Original: {orig_time:.4f}s")
    print(f"   Optimized: {opt_time:.4f}s")
    print(f"   Speedup: {orig_time/opt_time:.2f}x")
    
    # Test 3: Filter by municipality
    print("\n4. Filter by municipality...")
    municipality = original.data['municipality_code'].iloc[0]
    orig_time, orig_result = measure_time(original.filter_by_municipality, municipality)
    opt_time, opt_result = measure_time(optimized.filter_by_municipality, municipality)
    print(f"   Original: {orig_time:.4f}s")
    print(f"   Optimized: {opt_time:.4f}s")
    print(f"   Speedup: {orig_time/opt_time:.2f}x")
    
    # Test 4: Get procedures by diagnosis
    print("\n5. Get procedures by diagnosis...")
    diagnosis = original.data['diagnosis_code'].iloc[0]
    orig_time, orig_result = measure_time(original.get_procedures_by_diagnosis, diagnosis)
    opt_time, opt_result = measure_time(optimized.get_procedures_by_diagnosis, diagnosis)
    print(f"   Original: {orig_time:.4f}s")
    print(f"   Optimized: {opt_time:.4f}s")
    print(f"   Speedup: {orig_time/opt_time:.2f}x")
    
    # Test 5: Generate monthly report
    print("\n6. Generate monthly report...")
    orig_time, orig_result = measure_time(original.generate_monthly_report, 2023, 6)
    opt_time, opt_result = measure_time(optimized.generate_monthly_report, 2023, 6)
    print(f"   Original: {orig_time:.4f}s")
    print(f"   Optimized: {opt_time:.4f}s")
    print(f"   Speedup: {orig_time/opt_time:.2f}x")
    
    # Test 6: Search patient by ID
    print("\n7. Search patient by ID...")
    # Use min to avoid index out of bounds
    idx = min(500, len(original.data) - 1)
    patient_id = original.data['patient_id'].iloc[idx]
    orig_time, orig_result = measure_time(original.search_patient_by_id, patient_id)
    opt_time, opt_result = measure_time(optimized.search_patient_by_id, patient_id)
    print(f"   Original: {orig_time:.4f}s")
    print(f"   Optimized: {opt_time:.4f}s")
    print(f"   Speedup: {orig_time/opt_time:.2f}x")
    
    # Test 7: Find duplicate procedures
    print("\n8. Find duplicate procedures...")
    orig_time, orig_result = measure_time(original.find_duplicate_procedures)
    opt_time, opt_result = measure_time(optimized.find_duplicate_procedures)
    print(f"   Original: {orig_time:.4f}s")
    print(f"   Optimized: {opt_time:.4f}s")
    print(f"   Speedup: {orig_time/opt_time:.2f}x")
    
    print(f"\n{'='*70}")
    print("Benchmark complete!")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    # Run benchmark with different dataset sizes
    print("\nRunning benchmarks with increasing dataset sizes...\n")
    
    for size in [100, 1000, 5000]:
        run_benchmark(f'sample_data_{size}.csv', size)
        print("\n")
