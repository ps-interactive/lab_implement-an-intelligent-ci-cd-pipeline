#!/usr/bin/env python3
import sys

def check_import(module_name, package_name=None):
    if package_name is None:
        package_name = module_name
    try:
        __import__(module_name)
        print(f'[PASS] {package_name} is installed')
        return True
    except ImportError:
        print(f'[FAIL] {package_name} is NOT installed')
        return False

print('Checking Python environment...\n')

all_good = True
all_good &= check_import('pandas')
all_good &= check_import('numpy')
all_good &= check_import('sklearn', 'scikit-learn')

print('\n' + '='*40)
if all_good:
    print('[PASS] Environment validation PASSED')
else:
    print('[FAIL] Environment validation FAILED')
    print('\nRun this command to fix:')
    print('sudo dnf install -y python3-pip')
    print('pip3 install --user pandas numpy scikit-learn')
    sys.exit(1)
