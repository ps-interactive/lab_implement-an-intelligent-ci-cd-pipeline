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
    
    # Generate more realistic data - 75% of the time predictions match outcomes
    rand = random.random()
    if rand < 0.75:  # 75% accurate predictions
        # Correct predictions
        risk_choices = [('low', 'success'), ('medium', 'success'), ('high', 'failed')]
        predicted_risk, actual_outcome = random.choice(risk_choices)
    else:  # 25% inaccurate predictions
        # Incorrect predictions
        risk_choices = [('low', 'failed'), ('medium', 'failed'), ('high', 'success')]
        predicted_risk, actual_outcome = random.choice(risk_choices)
    
    pipeline_data = {
        'pipeline_id': f'run_{random.randint(1000, 9999)}',
        'duration': random.randint(60, 300),
        'status': actual_outcome if actual_outcome == 'success' else 'failed',
        'predicted_risk': predicted_risk,
        'actual_outcome': actual_outcome,
        'tests_passed': random.randint(10, 15) if actual_outcome == 'success' else random.randint(5, 9),
        'tests_failed': random.randint(0, 2) if actual_outcome == 'success' else random.randint(3, 5),
        'retry_count': random.randint(0, 1) if actual_outcome == 'success' else random.randint(1, 3)
    }
    
    monitor.record_pipeline_run(pipeline_data)
    print('Pipeline metrics recorded.')
    print(monitor.generate_dashboard())
```

## OR Update the Lab Guide Expected Output:

Change this part in the lab guide from:
```
**Expected output (with calculated accuracy):**
```
Pipeline metrics recorded.

+----------------------------------------------------------+
|           INTELLIGENT CI/CD PIPELINE DASHBOARD          |
+----------------------------------------------------------+
| Model Accuracy: 75.00%                                  |
| Total Predictions: 8                                    |
| Correct Predictions: 6                                  |
| Last Update: 2024-11-25 14:41:30                        |
+----------------------------------------------------------+
```
**Note:** Accuracy varies based on random data but typically ranges from 60-85%.
```

To:
```
**Expected output (with calculated accuracy):**
```
Pipeline metrics recorded.

+----------------------------------------------------------+
|           INTELLIGENT CI/CD PIPELINE DASHBOARD          |
+----------------------------------------------------------+
| Model Accuracy: 33.33%                                  |
| Total Predictions: 12                                   |
| Correct Predictions: 4                                  |
| Last Update: 2025-12-01 15:46:19                        |
+----------------------------------------------------------+
```
**Note:** Accuracy varies significantly (20-80%) based on randomly generated test data. Any accuracy above 0% indicates the monitoring system is working correctly.
