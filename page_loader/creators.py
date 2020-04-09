import re
import os
import logging
import traceback
from page_loader.known_error import KnownError


(TEXT, BIN) = ('text', 'bin')


def create_name(name, ending):
    return re.sub(r'[^0-9a-zA-Z]', '-', name) + ending


def create_dir(full_dir_name):
    try:
        os.mkdir(full_dir_name)
    except IOError as error:
        logging.debug(traceback.format_exc(10))
        logging.error("Can't create directory {}".format(full_dir_name))
        raise KnownError() from error


def create_file(full_file_name, content, format):
    access = "w" if format == TEXT else 'wb'
    logging.info("Saving {}".format(full_file_name))
    try:
        with open(full_file_name, access) as output_file:
            output_file.write(content)
    except IOError as error:
        logging.debug(traceback.format_exc(10))
        logging.error("Can't create file {}".format(full_file_name))
        raise KnownError() from error
