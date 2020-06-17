import requests
from os import path
import boto3
if __name__ == '__main__':
    s3_client = boto3.client('s3',
                             region_name='ap-east-1',
                             aws_access_key_id='AKIAXS73WH3R3G77ZWBJ',
                             aws_secret_access_key='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')

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
            r = requests.get(url, allow_redirects=True)
            print('writing content...')
            with open(f_path, 'wb') as f:
                f.write(r.content)
            s3_client.upload_file(f_path, 'de0ch-twitter-archive', f_name)