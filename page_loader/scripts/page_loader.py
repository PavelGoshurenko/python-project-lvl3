#!/usr/bin/env python3
import argparse
from page_loader.page_loader import page_loader
from page_loader.logger import log_config
import sys
from page_loader.known_error import KnownError


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
    log_config(args.log_level)
    try:
        page_loader(args.url, args.output)
    except KnownError:
        sys.exit(1)


if __name__ == '__main__':
    main()
