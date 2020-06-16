import requests
from os import path
import boto3
if __name__ == '__main__':
    with open('archive_links.txt') as links_f:
        for url in links_f:
            url = url.strip()
            url = 'https://file-examples.com/wp-content/uploads/2019/09/file-sample_300kB.rtf'
            if not url:
                continue
            f_name = url.rsplit('/', 1)[-1]
            f_path = path.join('downloads', f_name)
            print(f_name)
            print(url)
            # below is downloading content

            with open(f_path, 'wb') as f:
                response = requests.get(url, allow_redirects=True)
                total_length = response.headers.get('content-length')

                if total_length is None:  # no content length header
                    f.write(response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        done = int(50 * dl / total_length)
                        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                        sys.stdout.flush()
