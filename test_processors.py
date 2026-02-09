"""
Unit tests for healthcare data processors
"""
import pytest
import pandas as pd
import os
from healthcare_processor import HealthcareDataProcessor
from healthcare_processor_optimized import OptimizedHealthcareDataProcessor
from generate_data import generate_sample_data


@pytest.fixture
def test_data_file(tmp_path):
    """Create temporary test data file"""
    data_file = tmp_path / "test_data.csv"
    generate_sample_data(100, str(data_file))
    return str(data_file)


@pytest.fixture
def original_processor(test_data_file):
    """Initialize original processor with test data"""
    processor = HealthcareDataProcessor(test_data_file)
    processor.load_data()
    return processor


@pytest.fixture
def optimized_processor(test_data_file):
    """Initialize optimized processor with test data"""
    processor = OptimizedHealthcareDataProcessor(test_data_file)
    processor.load_data()
    return processor


class TestDataLoading:
    """Test data loading functionality"""
    
    def test_original_loads_data(self, original_processor):
        assert original_processor.data is not None
        assert len(original_processor.data) > 0
    
    def test_optimized_loads_data(self, optimized_processor):
        assert optimized_processor.data is not None
        assert len(optimized_processor.data) > 0


class TestCostCalculations:
    """Test cost calculation methods"""
    
    def test_calculate_total_cost_per_patient(self, original_processor, optimized_processor):
        orig_result = original_processor.calculate_total_cost_per_patient()
        opt_result = optimized_processor.calculate_total_cost_per_patient()
        
        # Results should be equivalent
        assert len(orig_result) == len(opt_result)
        for patient_id in orig_result:
            assert orig_result[patient_id] == pytest.approx(opt_result[patient_id], rel=1e-5)
    
    def test_get_top_expensive_procedures(self, original_processor, optimized_processor):
        orig_result = original_processor.get_top_expensive_procedures(5)
        opt_result = optimized_processor.get_top_expensive_procedures(5)
        
        assert len(orig_result) == len(opt_result)
        # Top procedures should be the same (order matters)
        for i in range(len(orig_result)):
            assert orig_result[i]['cost'] == pytest.approx(opt_result[i]['cost'], rel=1e-5)


class TestFiltering:
    """Test data filtering methods"""
    
    def test_filter_by_municipality(self, original_processor, optimized_processor):
        municipality = original_processor.data['municipality_code'].iloc[0]
        
        orig_result = original_processor.filter_by_municipality(municipality)
        opt_result = optimized_processor.filter_by_municipality(municipality)
        
        assert len(orig_result) == len(opt_result)
    
    def test_get_procedures_by_diagnosis(self, original_processor, optimized_processor):
        diagnosis = original_processor.data['diagnosis_code'].iloc[0]
        
        orig_result = original_processor.get_procedures_by_diagnosis(diagnosis)
        opt_result = optimized_processor.get_procedures_by_diagnosis(diagnosis)
        
        assert len(orig_result) == len(opt_result)


class TestSearch:
    """Test search functionality"""
    
    def test_search_patient_by_id(self, original_processor, optimized_processor):
        patient_id = original_processor.data['patient_id'].iloc[0]
        
        orig_result = original_processor.search_patient_by_id(patient_id)
        opt_result = optimized_processor.search_patient_by_id(patient_id)
        
        assert orig_result is not None
        assert opt_result is not None
        assert orig_result['patient_id'] == opt_result['patient_id']
    
    def test_search_nonexistent_patient(self, optimized_processor):
        result = optimized_processor.search_patient_by_id('NONEXISTENT')
        assert result is None


class TestReports:
    """Test report generation"""
    
    def test_generate_monthly_report(self, original_processor, optimized_processor):
        orig_report = original_processor.generate_monthly_report(2023, 6)
        opt_report = optimized_processor.generate_monthly_report(2023, 6)
        
        # Both should have same structure
        assert 'admissions' in orig_report
        assert 'total_cost' in orig_report
        assert 'unique_patients' in orig_report
        
        # Values should match
        assert orig_report['admissions'] == opt_report['admissions']
        assert orig_report['total_cost'] == pytest.approx(opt_report['total_cost'], rel=1e-5)
        assert orig_report['unique_patients'] == opt_report['unique_patients']
    
    def test_calculate_average_stay_duration(self, optimized_processor):
        avg_stay = optimized_processor.calculate_average_stay_duration()
        assert avg_stay > 0
        assert avg_stay < 365  # Reasonable range


class TestExport:
    """Test data export functionality"""
    
    def test_export_to_json(self, optimized_processor, tmp_path):
        output_file = tmp_path / "export.json"
        optimized_processor.export_to_json(str(output_file))
        
        assert output_file.exists()
        assert output_file.stat().st_size > 0


class TestDuplicates:
    """Test duplicate detection"""
    
    def test_find_duplicate_procedures(self, optimized_processor):
        duplicates = optimized_processor.find_duplicate_procedures()
        # Should return a list (may be empty if no duplicates)
        assert isinstance(duplicates, list)


class TestNewFeatures:
    """Test new optimized features"""
    
    def test_get_statistics_summary(self, optimized_processor):
        stats = optimized_processor.get_statistics_summary()
        
        assert 'total_records' in stats
        assert 'total_cost' in stats
        assert 'average_cost' in stats
        assert 'unique_patients' in stats
        assert stats['total_records'] > 0
