#!/usr/bin/env python3
import argparse
from page_loader.page_loader import page_loader
from page_loader import logger
import logging


def main():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('url', type=str)
    parser.add_argument('-o', '--output', help='set path for saving')
    args = parser.parse_args()
    logging.basicConfig(filename="page_loader.log", level=logging.DEBUG)
    logging.debug("This is a debug message")
    logging.info("Informational message")
    logging.error("An error has happened!")
    page_loader(args.url, args.output)


if __name__ == '__main__':
    main()
