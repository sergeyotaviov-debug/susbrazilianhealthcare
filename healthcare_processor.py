"""
Brazilian Healthcare (SUS) Data Processor
This module processes patient admission and procedure data from DATASUS.
"""
import pandas as pd
import json
import time
from typing import List, Dict, Any


class HealthcareDataProcessor:
    """Processes healthcare data with various inefficiencies"""
    
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.data = None
        self.cache = {}
    
    def load_data(self):
        """Load patient admission data"""
        # Inefficiency: Loading entire dataset into memory without chunking
        self.data = pd.read_csv(self.data_file)
        return self.data
    
    def calculate_total_cost_per_patient(self) -> Dict[str, float]:
        """Calculate total cost for each patient"""
        # Inefficiency: Using iterrows() instead of vectorized operations
        patient_costs = {}
        for index, row in self.data.iterrows():
            patient_id = row['patient_id']
            cost = row['procedure_cost']
            
            if patient_id in patient_costs:
                patient_costs[patient_id] += cost
            else:
                patient_costs[patient_id] = cost
        
        return patient_costs
    
    def get_procedures_by_diagnosis(self, diagnosis_code: str) -> List[Dict]:
        """Get all procedures for a specific diagnosis"""
        # Inefficiency: Filtering data row by row instead of using pandas filtering
        procedures = []
        for index, row in self.data.iterrows():
            if row['diagnosis_code'] == diagnosis_code:
                procedures.append({
                    'patient_id': row['patient_id'],
                    'procedure': row['procedure_name'],
                    'cost': row['procedure_cost'],
                    'date': row['admission_date']
                })
        return procedures
    
    def calculate_average_stay_duration(self) -> float:
        """Calculate average hospital stay duration"""
        # Inefficiency: Using list comprehension when pandas operation would be better
        durations = []
        for index, row in self.data.iterrows():
            duration = row['discharge_date'] - row['admission_date']
            durations.append(duration)
        
        return sum(durations) / len(durations) if durations else 0
    
    def get_top_expensive_procedures(self, n: int = 10) -> List[Dict]:
        """Get top N most expensive procedures"""
        # Inefficiency: Sorting in Python instead of using pandas built-in sorting
        procedures = []
        for index, row in self.data.iterrows():
            procedures.append({
                'procedure': row['procedure_name'],
                'cost': row['procedure_cost'],
                'patient_id': row['patient_id']
            })
        
        # Bubble sort - extremely inefficient for large datasets
        for i in range(len(procedures)):
            for j in range(len(procedures) - 1 - i):
                if procedures[j]['cost'] < procedures[j + 1]['cost']:
                    procedures[j], procedures[j + 1] = procedures[j + 1], procedures[j]
        
        return procedures[:n]
    
    def filter_by_municipality(self, municipality_code: str) -> pd.DataFrame:
        """Filter data by municipality"""
        # Inefficiency: Creating new DataFrame with append in loop
        filtered_data = pd.DataFrame()
        for index, row in self.data.iterrows():
            if row['municipality_code'] == municipality_code:
                filtered_data = filtered_data.append(row, ignore_index=True)
        
        return filtered_data
    
    def search_patient_by_id(self, patient_id: str) -> Dict:
        """Search for patient by ID"""
        # Inefficiency: Linear search through all records every time
        for index, row in self.data.iterrows():
            if row['patient_id'] == patient_id:
                return row.to_dict()
        return None
    
    def generate_monthly_report(self, year: int, month: int) -> Dict[str, Any]:
        """Generate monthly statistics report"""
        # Inefficiency: Multiple iterations over the same data
        report = {}
        
        # Count admissions
        admission_count = 0
        for index, row in self.data.iterrows():
            admission_date = pd.to_datetime(row['admission_date'])
            if admission_date.year == year and admission_date.month == month:
                admission_count += 1
        report['admissions'] = admission_count
        
        # Calculate total cost
        total_cost = 0
        for index, row in self.data.iterrows():
            admission_date = pd.to_datetime(row['admission_date'])
            if admission_date.year == year and admission_date.month == month:
                total_cost += row['procedure_cost']
        report['total_cost'] = total_cost
        
        # Count unique patients
        unique_patients = set()
        for index, row in self.data.iterrows():
            admission_date = pd.to_datetime(row['admission_date'])
            if admission_date.year == year and admission_date.month == month:
                unique_patients.add(row['patient_id'])
        report['unique_patients'] = len(unique_patients)
        
        return report
    
    def export_to_json(self, output_file: str):
        """Export data to JSON format"""
        # Inefficiency: Converting to JSON row by row
        records = []
        for index, row in self.data.iterrows():
            records.append(row.to_dict())
        
        with open(output_file, 'w') as f:
            json.dump(records, f, indent=2)
    
    def find_duplicate_procedures(self) -> List[Dict]:
        """Find potentially duplicate procedure entries"""
        # Inefficiency: O(n²) comparison
        duplicates = []
        data_list = self.data.to_dict('records')
        
        for i in range(len(data_list)):
            for j in range(i + 1, len(data_list)):
                if (data_list[i]['patient_id'] == data_list[j]['patient_id'] and
                    data_list[i]['procedure_name'] == data_list[j]['procedure_name'] and
                    data_list[i]['admission_date'] == data_list[j]['admission_date']):
                    duplicates.append({
                        'record1': i,
                        'record2': j,
                        'patient_id': data_list[i]['patient_id']
                    })
        
        return duplicates
