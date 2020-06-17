import requests
from os import path
import os
if __name__ == '__main__':
    try:
        os.mkdir('downloads')
    except FileExistsError:
        pass
    f_name = 'twitter_stream_2019_05_01.tar'
    url = 'https://archive.org/download/archiveteam-twitter-stream-2019-05/' + f_name
    print('getting content...')
    r = requests.get(url, allow_redirects=True)
    print('writing content...')
    with open(path.join('downloads', f_name), 'wb') as f:
        f.write(r.content)
