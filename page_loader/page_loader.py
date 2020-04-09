from urllib.parse import urlparse
import os
from bs4 import BeautifulSoup
from progress.bar import ChargingBar
from page_loader.creators import create_dir, create_file, create_name
from page_loader.creators import TEXT, BIN
from page_loader.requestor import get_content, OBLIGATORY, OPTIONAL


(LINK, SCRIPT, IMG) = ('link', 'script', 'img')
(SRC, HREF) = ('src', 'href')
SOURSE = {LINK: HREF, SCRIPT: SRC, IMG: SRC}


def page_loader(url, path):
    # naming
    if path is None:
        path = ""
    url_components = urlparse(url)
    address = url_components.netloc + url_components.path
    file_name = create_name(address, '.html')
    dir_name = create_name(address, '_files')
    full_file_name = os.path.join(path, file_name)
    full_dir_name = os.path.join(path, dir_name)
    create_dir(full_dir_name)
    # get main file content
    file_content = get_content(url, OBLIGATORY)
    # download resourses
    soup = BeautifulSoup(file_content, 'html.parser')
    files_count = len(soup.find_all([LINK, SCRIPT, IMG]))
    bar = ChargingBar('Loading:', suffix='%(percent)d%%', max=files_count)
    for tag_name, attribute in SOURSE.items():
        tags = soup.find_all([tag_name])
        for tag in tags:
            resourse_url = tag.get(attribute)
            if resourse_url and resourse_url[0] == '/':
                resourse_full_url = url_components._replace(path=resourse_url).geturl() # noqa E501
                (resourse_url_root, resourse_url_ext) = os.path.splitext(resourse_url[1:]) # noqa E501
                resourse_file_name = create_name(resourse_url_root, resourse_url_ext) # noqa E501
                full_resourse_name = os.path.join(full_dir_name, resourse_file_name) # noqa E501
                # get resource content
                resource_content = get_content(resourse_full_url, OPTIONAL)
                create_file(full_resourse_name, resource_content, BIN)
                # change url to local path
                tag[attribute] = os.path.join(dir_name, resourse_file_name)
            bar.next()
    bar.finish()
    new_text = soup.prettify()
    create_file(full_file_name, new_text, TEXT)
