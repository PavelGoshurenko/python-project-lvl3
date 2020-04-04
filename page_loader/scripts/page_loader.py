#!/usr/bin/env python3
import argparse
from page_loader.page_loader import page_loader


def main():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('url', type=str)
    parser.add_argument('-o', '--output', help='set path for saving')
    args = parser.parse_args()
    page_loader(args.url, args.output)


if __name__ == '__main__':
    main()
