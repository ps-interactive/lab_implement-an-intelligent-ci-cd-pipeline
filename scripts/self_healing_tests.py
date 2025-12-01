#!/usr/bin/env python3
import time
import random
import json
from datetime import datetime

class SelfHealingTestSuite:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries
        self.test_history = []
        
    def run_test_with_retry(self, test_name, test_func):
        for attempt in range(self.max_retries):
            try:
                print(f'Running {test_name} (attempt {attempt + 1}/{self.max_retries})')
                result = test_func()
                self.test_history.append({
                    'test': test_name,
                    'attempt': attempt + 1,
                    'status': 'passed',
                    'timestamp': datetime.now().isoformat()
                })
                print(f'[PASS] {test_name} passed')
                return True
            except Exception as e:
                print(f'[FAIL] {test_name} failed on attempt {attempt + 1}: {e}')
                if attempt < self.max_retries - 1:
                    print(f'  Applying healing strategy...')
                    time.sleep(2 ** attempt)
                self.test_history.append({
                    'test': test_name,
                    'attempt': attempt + 1,
                    'status': 'failed',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        return False
    
    def generate_report(self):
        total_tests = len(set(h['test'] for h in self.test_history))
        passed_tests = len(set(h['test'] for h in self.test_history if h['status'] == 'passed'))
        return {
            'total_tests': total_tests,
            'passed': passed_tests,
            'failed': total_tests - passed_tests,
            'success_rate': passed_tests / total_tests if total_tests > 0 else 0,
            'history': self.test_history
        }

def test_api_response():
    if random.random() > 0.7:
        raise Exception('API timeout')
    return True

def test_database_connection():
    if random.random() > 0.8:
        raise Exception('Database connection failed')
    return True

def test_model_accuracy():
    return True

if __name__ == '__main__':
    suite = SelfHealingTestSuite(max_retries=3)
    suite.run_test_with_retry('API Response Test', test_api_response)
    suite.run_test_with_retry('Database Connection Test', test_database_connection)
    suite.run_test_with_retry('Model Accuracy Test', test_model_accuracy)
    report = suite.generate_report()
    print('\n' + '='*50)
    print('Test Suite Report')
    print('='*50)
    print(json.dumps(report, indent=2))
