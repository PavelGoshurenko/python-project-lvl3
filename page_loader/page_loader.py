#!/usr/bin/env python3
import requests
from urllib.parse import urlparse
import re
import os


def page_loader(url, path):
    url_components = urlparse(url)
    address = url_components.netloc + url_components.path
    file_name = re.sub(r'[^0-9a-zA-Z]', '-', address) + '.html'
    if path is None:
        full_path = file_name
    else:
        full_path = os.path.join(path, file_name)
    print(full_path)
    r = requests.get(url)
    text = r.text
    with open(full_path, "w") as output_file:
        output_file.write(text)
