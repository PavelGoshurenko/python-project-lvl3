import pytest
from page_loader.page_loader import page_loader
import tempfile
import os


 
CORRECT_FILE = './tests/fixtures/output.html'
TEST_URL = 'https://www.python.org'
TEMP_FILE_NAME = 'www-python-org.html'


def test():
    with open(CORRECT_FILE, 'r') as correct_file:
        correct_result = correct_file.read()
    with tempfile.TemporaryDirectory() as temp_dir:
        page_loader(TEST_URL, temp_dir)
        full_path = os.path.join(temp_dir, TEMP_FILE_NAME)
        with open(full_path, 'r') as test_file:
            test_result = test_file.read()
    assert correct_result == test_result
