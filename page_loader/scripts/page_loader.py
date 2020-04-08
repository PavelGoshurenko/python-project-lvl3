#!/usr/bin/env python3
import argparse
from page_loader.page_loader import page_loader
# from page_loader import logger
import logging
import sys
from page_loader.page_loader import KnownError


def main():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('url', type=str)
    parser.add_argument('-o', '--output', help='set path for saving')
    args = parser.parse_args()
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename="page_loader.log", level=logging.DEBUG) # noqa 501
    try:
        page_loader(args.url, args.output)
    except KnownError:
        print("catch known error")
        sys.exit(1)


if __name__ == '__main__':
    main()
