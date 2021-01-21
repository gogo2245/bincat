from bs4 import BeautifulSoup
from requests import request
from utils import *
import shutil
import os


def prepare_directories(architectures, output_dir):
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)
    os.mkdir(os.path.join(output_dir, '_working'))
    for architecture in architectures:
        check_if_dir_exists_or_create(os.path.join(output_dir, architecture))


def run(config):
    architectures = config['architectures']
    output_dir = config['output_dir']
    # Get links for all pages
    page = request('GET', 'https://beginnersbook.com/2015/02/simple-c-programs/')
    soup = BeautifulSoup(page.content, features='html.parser')
    main_soup = soup.find('div', {'class': 'entry-content'})
    links = []
    counter = 0

    prepare_directories(architectures, output_dir)

    # first and last links are irrelevant
    for href_soup in main_soup.find_all('a', href=True)[1:-1]:
        links.append(href_soup['href'])

    # Get code from page
    for link in links:
        page = request('GET', link)
        soup = BeautifulSoup(page.content, features='html.parser')
        code_tag = soup.find('pre')
        f = open(os.path.join(output_dir, '_working', str(counter) + '.c'), 'wb')
        f.write(code_tag.text.encode('utf8'))
        counter += 1
        f.close()

    _, _, files = next(os.walk(os.path.join(output_dir, '_working')))
    for f in files:
        for architecture in architectures:
            command = architectures[architecture]
            command = command.replace('OUTPUT_PATH', os.path.join(output_dir, architecture, f.split('.')[0]))
            command = command.replace('INPUT_PATH', os.path.join(output_dir, '_working', f))
            if os.system(command) != 0:
                print('Compilation failed skipping', architecture, f)

    shutil.rmtree(os.path.join(output_dir, '_working'))
