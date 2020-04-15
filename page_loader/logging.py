import logging


class KnownError(Exception):
    pass


def configure(level):
    logging.basicConfig(
        format='%(asctime)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S'
        )
    log = logging.getLogger()
    log.setLevel(level)
