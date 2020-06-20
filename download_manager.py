import requests
from os import path
import boto3
import sys
import progressbar
import coloredlogs
import logging
import os
import multiprocessing


def worker(queue):
    while True:
        url = queue.get()
        download_file(url)
        queue.task_done()


def download_file(url):
    url = url.strip()
    if not url:
        return
    f_name = url.rsplit('/', 1)[-1]
    f_path = path.join('downloads', f_name)
    if os.path.isfile(f_path):
        logging.debug('file already downloaded: ' + url)
        return
    logging.info('started downloading: ' + url)
    # below is downloading content

    with open(f_path, 'wb') as f:
        response = requests.get(url, allow_redirects=True, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            for data in response.iter_content(chunk_size=4096):
                f.write(data)
        logging.info('finished downloading: ' + url)


if __name__ == '__main__':
    coloredlogs.install()
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    queue = multiprocessing.JoinableQueue()
    for i in range(50):
        multiprocessing.Process(target=worker, args=(queue,), daemon=True).start()

    with open('archive_links_raw.txt') as links_f:
        for url in links_f:
            queue.put(url)

    queue.join()
    print('done')
