#!/usr/bin/env python3
import argparse
import sys

from page_loader import logging
from page_loader.logging import KnownError
from page_loader.page_loader import load_page


def main():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('url', type=str)
    parser.add_argument('-o', '--output', help='set path for saving', type=str)
    parser.add_argument(
        '-l',
        '--log_level',
        help='set logging level from DEBUG, INFO, WARNING, ERROR, CRITICAL',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='WARNING')
    args = parser.parse_args()
    logging.configure(args.log_level)
    try:
        load_page(args.url, args.output)
    except KnownError:
        sys.exit(1)


if __name__ == '__main__':
    main()
