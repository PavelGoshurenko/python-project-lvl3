import os
import tempfile

import pytest
import requests_mock
from page_loader import logging
from page_loader.logging import KnownError
from page_loader.network import OBLIGATORY, OPTIONAL, get_content
from page_loader.page_loader import load_page, download_resources

# A static html file that has not changed since 1997
TEST_URL = 'http://endoftheinternet.com/'
TEMP_FILE_NAME = 'endoftheinternet-com-.html'
CORRECT_FILE = './tests/fixtures/output_html.html'
CORRECT_DIR = 'endoftheinternet-com-_files'
SIMPLE_PAGE_URL = 'https://httpbin.org/html'
SIMPLE_CORRECT_FILE = './tests/fixtures/output_simple'
TEST_IMAGE_URL = 'https://httpbin.org/image/jpeg'

INCORRECT_URL = 'https://httpbin.org/status/404'
INCORRECT_PASS = '/non/existent/path'


def test_get_page():
    logging.configure('DEBUG')
    with open(SIMPLE_CORRECT_FILE, 'rb') as correct_file:
        correct_result = correct_file.read()
    test_result = get_content(SIMPLE_PAGE_URL, OBLIGATORY)
    assert correct_result == test_result


def test_create_file():
    logging.configure('DEBUG')
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as m:
            m.get(TEST_URL, text='test')
            load_page(TEST_URL, temp_dir)
        full_path = os.path.join(temp_dir, TEMP_FILE_NAME)
        assert os.path.exists(full_path) == True


def test_create_dir():
    logging.configure('DEBUG')
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as m:
            m.get(TEST_URL, text='test')
            load_page(TEST_URL, temp_dir)
        resource_dir = os.path.join(temp_dir, CORRECT_DIR)
        assert os.path.isdir(resource_dir) == True


def test_html():
    logging.configure('DEBUG')
    with open(CORRECT_FILE, 'r') as correct_file:
        correct_result = correct_file.read()
    with tempfile.TemporaryDirectory() as temp_dir:
        load_page(TEST_URL, temp_dir)
        full_path = os.path.join(temp_dir, TEMP_FILE_NAME)
        with open(full_path, 'r') as test_file:
            test_result = test_file.read()
    assert correct_result == test_result


def test_load_resource():
    logging.configure('DEBUG')
    with tempfile.TemporaryDirectory() as temp_dir:
        full_path = os.path.join(temp_dir, 'image.jpeg')
        download_resources(TEST_IMAGE_URL, temp_dir, [('/image/jpeg', 'image.jpeg')])
        assert os.path.exists(full_path) == True


def test_load_bad_resource():
    logging.configure('DEBUG')
    with tempfile.TemporaryDirectory() as temp_dir:
        full_path = os.path.join(temp_dir, 'image.jpeg')
        download_resources(TEST_IMAGE_URL, temp_dir, [('/noimage/jpeg', 'image.jpeg')])
        assert os.path.exists(full_path) == False

    
def test_errors():
    logging.configure('DEBUG')
    with pytest.raises(KnownError):
        with tempfile.TemporaryDirectory() as temp_dir:
            load_page(INCORRECT_URL, temp_dir)
    with pytest.raises(KnownError):
        load_page(TEST_URL, INCORRECT_PASS)
