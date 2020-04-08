import requests
from urllib.parse import urlparse
import re
import os
from bs4 import BeautifulSoup
import logging
import traceback


class KnownError(Exception):
    pass


(LINK, SCRIPT, IMG) = ('link', 'script', 'img')
(SRC, HREF) = ('src', 'href')
SOURSE = {LINK: HREF, SCRIPT: SRC, IMG: SRC}


def make_name(name, ending):
    return re.sub(r'[^0-9a-zA-Z]', '-', name) + ending


def page_loader(url, path):
    # naming
    if path is None:
        path = ""
    url_components = urlparse(url)
    address = url_components.netloc + url_components.path
    file_name = make_name(address, '.html')
    dir_name = make_name(address, '_files')
    full_file_name = os.path.join(path, file_name)
    full_dir_name = os.path.join(path, dir_name)
    try:
        os.mkdir(full_dir_name)
    except IOError as error:
        logging.debug(traceback.format_exc(10))
        logging.error("Can't create directory {}".format(full_dir_name))
        raise KnownError() from error
    # get main file content
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.RequestException as error:
        logging.error(error)
        raise requests.RequestException(error)
    file_content = r.text
    # download resourses
    soup = BeautifulSoup(file_content, 'html.parser')
    for tag_name, attribute in SOURSE.items():
        tags = soup.find_all([tag_name])
        for tag in tags:
            resourse_url = tag.get(attribute)
            if resourse_url and resourse_url[0] == '/':
                resourse_full_url = url_components._replace(path=resourse_url).geturl() # noqa E501
                r1 = requests.get(resourse_full_url)
                (resourse_url_root, resourse_url_ext) = os.path.splitext(resourse_url[1:]) # noqa E501
                resourse_file_name = make_name(resourse_url_root, resourse_url_ext) # noqa E501
                full_resourse_name = os.path.join(full_dir_name, resourse_file_name) # noqa E501
                logging.info("Save {}\nas {}".format(resourse_full_url, full_resourse_name)) # noqa E501
                with open(full_resourse_name, 'wb') as file:
                    file.write(r1.content)
                # change url to local path
                tag[attribute] = os.path.join(dir_name, resourse_file_name)
    new_text = soup.prettify()
    logging.info("Save {}\nas {}".format(url, full_file_name))
    try:
        with open(full_file_name, "w") as output_file:
            output_file.write(new_text)
    except IOError:
        logging.error("Can't create file {}".format(full_file_name))
        raise IOError("Can't create file {}".format(full_file_name))
