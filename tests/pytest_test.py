import pytest
from page_loader.page_loader import page_loader
import tempfile
import os
from page_loader.logger import log_config
from page_loader.known_error import KnownError


 
 # A static html file that has not changed since 1997
CORRECT_FILE = './tests/fixtures/output.html'
CORRECT_DIR = 'endoftheinternet-com-_files'
TEST_URL = 'http://endoftheinternet.com/'
TEMP_FILE_NAME = 'endoftheinternet-com-.html'

INCORRECT_URL = 'http://not_existent_url.com/'
INCORRECT_PASS = '/non/existent/path'


def test():
    log_config('DEBUG')
    with open(CORRECT_FILE, 'r') as correct_file:
        correct_result = correct_file.read()
    with tempfile.TemporaryDirectory() as temp_dir:
        page_loader(TEST_URL, temp_dir)
        full_path = os.path.join(temp_dir, TEMP_FILE_NAME)
        with open(full_path, 'r') as test_file:
            test_result = test_file.read()
        resource_dir = os.path.join(temp_dir, CORRECT_DIR)
        assert os.path.isdir(resource_dir) == True
    assert correct_result == test_result
    

def test_errors():
    log_config('DEBUG')
    with pytest.raises(KnownError):
        with tempfile.TemporaryDirectory() as temp_dir:
            page_loader(INCORRECT_URL, temp_dir)
    with pytest.raises(KnownError):
        page_loader(TEST_URL, INCORRECT_PASS)

