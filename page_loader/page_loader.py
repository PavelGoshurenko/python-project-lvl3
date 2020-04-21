import logging
import os
import re
import traceback
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from progress.bar import ChargingBar

from page_loader.logging import KnownError
from page_loader.network import OBLIGATORY, OPTIONAL, get_content

LINK, SCRIPT, IMG = 'link', 'script', 'img'
SRC, HREF = 'src', 'href'
SOURSE = {LINK: HREF, SCRIPT: SRC, IMG: SRC}
TEXT, BIN = 'text', 'bin'


def transform_name(name, ending):
    return re.sub(r'[^0-9a-zA-Z]', '-', name) + ending


def create_dir(full_dir_name):
    try:
        os.mkdir(full_dir_name)
    except IOError as error:
        logging.debug(traceback.format_exc(10))
        logging.error("Can't create directory {}".format(full_dir_name))
        raise KnownError() from error


def save_to_file(full_file_name, content, format):
    access = "w" if format == TEXT else 'wb'
    logging.info("Saving {}".format(full_file_name))
    try:
        with open(full_file_name, access) as output_file:
            output_file.write(content)
    except IOError as error:
        logging.debug(traceback.format_exc(10))
        logging.error("Can't create file {}".format(full_file_name))
        raise KnownError() from error


def download_resources(url, target_dir, resources):
    files_count = len(resources)
    url_components = urlparse(url)
    bar = ChargingBar('Loading:', suffix='%(percent)d%%', max=files_count)
    for resource in resources:
        (resource_url, resource_file_name) = resource
        resource_full_url = url_components._replace(path=resource_url).geturl() # noqa E501
        full_resource_name = os.path.join(target_dir, resource_file_name) # noqa E501
        resource_content = get_content(resource_full_url, OPTIONAL)
        if resource_content:
            save_to_file(full_resource_name, resource_content, BIN)
        bar.next()
    bar.finish()


def make_local(content, dir_name):
    soup = BeautifulSoup(content, 'html.parser')
    resources = []
    for tag_name, attribute in SOURSE.items():
        tags = soup.find_all([tag_name])
        for tag in tags:
            resource_url = tag.get(attribute)
            if resource_url and resource_url[0] == '/':
                (resource_url_root, resource_url_ext) = os.path.splitext(resource_url[1:]) # noqa E501
                resource_file_name = transform_name(resource_url_root, resource_url_ext) # noqa E501
                resources.append((resource_url, resource_file_name))
                # change url to local path
                tag[attribute] = os.path.join(dir_name, resource_file_name) # noqa E501
    new_content = soup.prettify()
    return (new_content, resources)


def load_page(url, path):
    path = "" if path is None else path
    url_components = urlparse(url)
    address = url_components.netloc + url_components.path
    file_name = transform_name(address, '.html')
    dir_name = transform_name(address, '_files')
    full_file_name = os.path.join(path, file_name)
    full_dir_name = os.path.join(path, dir_name)
    create_dir(full_dir_name)
    file_content = get_content(url, OBLIGATORY)
    new_content, resources = make_local(file_content, dir_name)
    save_to_file(full_file_name, new_content, TEXT)
    download_resources(url, full_dir_name, resources)
