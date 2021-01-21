from googleapiclient.discovery import build
import requests
import time
from utils import *
import os


# this downloads and saves images
def download_image(path, pic_url):
    with open(path, 'wb') as handle:
        response = requests.get(pic_url, stream=True)

        if not response.ok:
            handle.close()
            os.remove(path)
            return

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)


# google search
def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


def run(config):

    counter = 0
    prefix = str(int(time.time()))

    my_api_key = config['google_api_key']
    my_cse_id = config['google_cse_id']

    queries = config['queries']
    formats = config['formats']
    output_dir = config['output_dir']
    required_bytes = config['required_bytes']

    check_required_directories(output_dir)
    todo = {}
    for required_format in formats:
        check_if_dir_exists_or_create(os.path.join(output_dir, required_format))
        size = get_directory_size(os.path.join(output_dir, required_format))
        if size < required_bytes:
            todo[required_format] = required_bytes - size

    for f in todo:
        for q in queries:
            results = google_search(
                q, my_api_key, my_cse_id, searchType='image', fileType=f, num=10)
            results = list(map(lambda item: item['link'], results))

            for image_url in results:
                download_image(os.path.join(output_dir, f, prefix + '_' + str(counter) + '.' + f), image_url)
                counter += 1

            size = get_directory_size(os.path.join(output_dir, f))
            todo[f] = required_bytes - size
            if todo[f] < size:
                break

    not_finished = 0
    for i in todo:
        if todo[i] > 0:
            not_finished += 1

    if not_finished != 0:
        print('Not enough queries for required bytes. Please add other queries.')

