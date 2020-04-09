import logging


def log_config(level):
    logging.basicConfig(
        format='%(asctime)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S'
        )
    log = logging.getLogger()
    log.setLevel(level)
