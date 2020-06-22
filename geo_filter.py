# noinspection PyPackageRequirements
import json
import os
import bz2
import multiprocessing
import coloredlogs, logging
import pickle


def worker(q, ):
    while True:
        path, file_name = q.get()
        process_files(path, file_name)
        q.task_done()


def process_files(path, file_name):
    file_name_no_extension, file_extension = os.path.splitext(file_name)
    out_file_name = os.path.join('processed', os.path.relpath(path, start='untarred'), file_name_no_extension)
    os.makedirs(os.path.dirname(out_file_name), exist_ok=True)
    with open(out_file_name, 'w') as out_file:
        with open(os.path.join(path, file_name), 'rb') as file:
            decompressed_string = bz2.decompress(file.read())
            lines = decompressed_string.decode('utf-8').split('\n')
            tweets = []
            for line in lines:
                try:
                    if not line.strip():
                        continue
                    tweet = json.loads(line)
                    try:
                        if tweet['place']['country_code']:
                            tweets.append(tweet)
                    except (KeyError, TypeError):
                        pass
                except Exception as e:
                    logging.exception(e)
        out_file.write(json.dumps(tweets))
        logging.info('finished ' + os.path.join(path, file_name))


if __name__ == '__main__':
    coloredlogs.install()
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    q = multiprocessing.JoinableQueue()
    os.makedirs('processed', exist_ok=True)
    for i in range(os.cpu_count() - 1):
        p = multiprocessing.Process(target=worker, args=(q, ), daemon=True)
        p.start()
    for path, dirs, files in os.walk('untarred'):
        for file_name in files:
            if file_name.endswith('.json.bz2'):
                q.put((path, file_name))
    q.join()
    print('done, safe to ctrl-c if it does not exit automatically')