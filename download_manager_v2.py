import requests
from os import path
import boto3
import sys
import progressbar
if __name__ == '__main__':
    with open('archive_links.txt') as links_f:
        for url in links_f:
            url = url.strip()
            if not url:
                continue
            f_name = url.rsplit('/', 1)[-1]
            f_path = path.join('downloads', f_name)
            print(f_name)
            print(url)
            # below is downloading content

            with open(f_path, 'wb') as f:
                response = requests.get(url, allow_redirects=True, stream=True)
                total_length = response.headers.get('content-length')

                if total_length is None:  # no content length header
                    f.write(response.content)
                else:
                    total_length = int(total_length)
                    with progressbar.ProgressBar(max_value=total_length) as bar:
                        dl = 0
                        for data in response.iter_content(chunk_size=4096):
                            dl += len(data)
                            f.write(data)
                            # noinspection PyBroadException
                            try:
                                bar.update(dl)
                            except:
                                pass
