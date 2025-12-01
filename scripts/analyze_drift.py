#!/usr/bin/env python3
import csv
import os

metrics_file = 'monitoring/metrics.csv'

if os.path.exists(metrics_file):
    with open(metrics_file, 'r') as f:
        reader = list(csv.DictReader(f))
    
    total_runs = len(reader)
    
    # Calculate accuracy for recent runs
    recent_runs = reader[-10:] if len(reader) >= 10 else reader
    correct = sum(1 for r in recent_runs 
                  if (r['predicted_risk'] == 'high' and r['actual_outcome'] == 'failed') or
                     (r['predicted_risk'] != 'high' and r['actual_outcome'] == 'success'))
    accuracy = correct / len(recent_runs) if recent_runs else 0
    
    print('Model Performance Analysis')
    print('='*40)
    print(f'Total pipeline runs: {total_runs}')
    print(f'Recent accuracy: {accuracy:.1%}')
    
    if accuracy < 0.70:
        print('WARNING: Model drift detected!')
        print('Recommendation: Retrain model')
    elif total_runs < 5:
        print('Status: Need more runs for drift detection')
    else:
        print('Status: Model performing within acceptable range')
    
    print('[PASS] Analysis complete')
else:
    print('No metrics data available')
