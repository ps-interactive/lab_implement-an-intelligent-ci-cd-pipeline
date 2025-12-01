#!/usr/bin/env python3
import json
import csv
import os
from datetime import datetime
import random

class PipelineMonitor:
    def __init__(self, metrics_file='monitoring/metrics.csv'):
        self.metrics_file = metrics_file
        os.makedirs(os.path.dirname(metrics_file), exist_ok=True)
        self._initialize_csv()
    
    def _initialize_csv(self):
        if not os.path.exists(self.metrics_file):
            with open(self.metrics_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'pipeline_id', 'duration', 'status', 
                               'predicted_risk', 'actual_outcome', 'tests_passed', 
                               'tests_failed', 'retry_count'])
    
    def record_pipeline_run(self, pipeline_data):
        with open(self.metrics_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                pipeline_data.get('timestamp', datetime.now().isoformat()),
                pipeline_data.get('pipeline_id', 'unknown'),
                pipeline_data.get('duration', 0),
                pipeline_data.get('status', 'unknown'),
                pipeline_data.get('predicted_risk', 'unknown'),
                pipeline_data.get('actual_outcome', 'unknown'),
                pipeline_data.get('tests_passed', 0),
                pipeline_data.get('tests_failed', 0),
                pipeline_data.get('retry_count', 0)
            ])
    
    def analyze_accuracy(self):
        if not os.path.exists(self.metrics_file):
            return {'error': 'No metrics data available'}
        
        correct_predictions = 0
        total_predictions = 0
        
        with open(self.metrics_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['predicted_risk'] != 'unknown' and row['actual_outcome'] != 'unknown':
                    total_predictions += 1
                    if (row['predicted_risk'] == 'high' and row['actual_outcome'] == 'failed') or \
                       (row['predicted_risk'] in ['low', 'medium'] and row['actual_outcome'] == 'success'):
                        correct_predictions += 1
        
        accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
        
        return {
            'accuracy': accuracy,
            'total_predictions': total_predictions,
            'correct_predictions': correct_predictions,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def generate_dashboard(self):
        analysis = self.analyze_accuracy()
        dashboard = '''\n+----------------------------------------------------------+
|           INTELLIGENT CI/CD PIPELINE DASHBOARD          |
+----------------------------------------------------------+
| Model Accuracy: {:.2%}                                   |
| Total Predictions: {}                                    |
| Correct Predictions: {}                                  |
| Last Update: {}                                          |
+----------------------------------------------------------+
'''.format(
            analysis.get('accuracy', 0),
            analysis.get('total_predictions', 0),
            analysis.get('correct_predictions', 0),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        return dashboard

if __name__ == '__main__':
    monitor = PipelineMonitor()
    pipeline_data = {
        'pipeline_id': f'run_{random.randint(1000, 9999)}',
        'duration': random.randint(60, 300),
        'status': random.choice(['success', 'failed']),
        'predicted_risk': random.choice(['low', 'medium', 'high']),
        'actual_outcome': random.choice(['success', 'failed']),
        'tests_passed': random.randint(5, 15),
        'tests_failed': random.randint(0, 3),
        'retry_count': random.randint(0, 2)
    }
    monitor.record_pipeline_run(pipeline_data)
    print('Pipeline metrics recorded.')
    print(monitor.generate_dashboard())
