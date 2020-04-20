import logging
import traceback

import requests

from page_loader.logging import KnownError

OBLIGATORY, OPTIONAL = 'obligatory', 'optional'


def get_content(url, priority):
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.RequestException as error:
        logging.debug(traceback.format_exc(10))
        if priority == OBLIGATORY:
            logging.error("Can't get {}".format(url))
            raise KnownError() from error
        else:
            # Some resources may not be available.
            # Let's give the program opportunity to finish.
            logging.debug("Can't get {}".format(url))
            return
    return r.content
