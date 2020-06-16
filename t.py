import requests
from os import path
import os

if __name__ == '__main__':

    for i in range(1, 32):
        f_name = 'twitter_stream_2019_05_%s.tar' % (str(i).zfill(2))
        url = 'https://archive.org/download/archiveteam-twitter-stream-2019-05/' + f_name
        print(url)
        print('getting content...')
        r = requests.get(url, allow_redirects=True)
        print('writing content...')
        with open(path.join('downloads', f_name), 'wb') as f:
            f.write(r.content)
