"""
Sample data generator for testing the healthcare processor
"""
import pandas as pd
import random
from datetime import datetime, timedelta


def generate_sample_data(num_records: int = 1000, output_file: str = 'sample_data.csv'):
    """Generate sample healthcare data for testing"""
    
    diagnoses = ['U07.1', 'I10', 'E11', 'J18.9', 'N18.9', 'I25.1', 'K70.3', 'C50.9']
    procedures = [
        'Consulta médica',
        'Exame de sangue',
        'Raio-X',
        'Cirurgia cardíaca',
        'Internação UTI',
        'Hemodiálise',
        'Quimioterapia'
    ]
    municipalities = ['3550308', '3304557', '4106902', '2927408', '2611606']
    
    data = []
    
    for i in range(num_records):
        patient_id = f'P{random.randint(1000, 9999):04d}'
        admission_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 364))
        stay_duration = random.randint(1, 30)
        discharge_date = admission_date + timedelta(days=stay_duration)
        
        data.append({
            'patient_id': patient_id,
            'admission_date': admission_date.strftime('%Y-%m-%d'),
            'discharge_date': discharge_date.strftime('%Y-%m-%d'),
            'diagnosis_code': random.choice(diagnoses),
            'procedure_name': random.choice(procedures),
            'procedure_cost': round(random.uniform(100, 10000), 2),
            'municipality_code': random.choice(municipalities)
        })
    
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Generated {num_records} records in {output_file}")
    return df


if __name__ == '__main__':
    generate_sample_data(1000)
