"""
Configuration for pytest test runner
"""
import os
import sys
import django
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent

# Add project to path
sys.path.insert(0, str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xml_manager.settings')
django.setup()


def pytest_configure(config):
    """Configure pytest"""
    import logging
    
    # Disable logging during tests
    logging.disable(logging.CRITICAL)
