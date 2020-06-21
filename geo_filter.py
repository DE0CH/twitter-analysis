# noinspection PyPackageRequirements
import json
import os
import bz2
import multiprocessing
import coloredlogs, logging
import pickle


def worker(q, geo_filtered_dict):
    while True:
        path, dirs, files = q.get()
        process_files(path, dirs, files, geo_filtered_dict)
        q.task_done()


def process_files(path, dirs, files, geo_filtered_dict):
    for file_name in files:
        if os.path.join(path, file_name) in geo_filtered_dict:
            continue
        file_name_no_extension, file_extension = os.path.splitext(file_name)
        out_file_name = os.path.join('processed', os.path.relpath(path, start='untarred'), file_name_no_extension)
        os.makedirs(os.path.dirname(out_file_name), exist_ok=True)
        with open(out_file_name, 'w') as out_file:
            if file_name.endswith('.json.bz2'):
                with open(os.path.join(path, file_name), 'rb') as file:
                    decompressed_string = bz2.decompress(file.read())
                    lines = decompressed_string.decode('utf-8').split('\n')
                    for line in lines:
                        if not line.strip():
                            continue
                        tweet = json.loads(line)
                        if tweet.get('place', None) is not None and tweet['place']['country_code']:
                            out_file.write(line)
                logging.info('finished ' + os.path.join(path, file_name))
        geo_filtered_dict[os.path.join(path, file_name)] = True


if __name__ == '__main__':
    try:
        with open('geo_filtered.pkl', 'rb') as f:
            geo_filtered = pickle.load(f)
    except FileNotFoundError:
        geo_filtered = set()
    coloredlogs.install()
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    q = multiprocessing.JoinableQueue()
    manager = multiprocessing.Manager()
    geo_filtered_dict = manager.dict()
    for key in geo_filtered:
        geo_filtered_dict[key] = True
    try:
        os.makedirs('processed')
    except FileExistsError:
        pass
    processes = []
    for i in range(100):
        p = multiprocessing.Process(target=worker, args=(q, geo_filtered_dict))
        processes.append(p)
        p.start()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'twitter-sentiment-analysis-f22ce784b0a8.json'
    try:
        for path, dirs, files in os.walk('untarred'):
            q.put((path, dirs, files))
        q.join()
    except KeyboardInterrupt:
        pass
    finally:
        with open('geo_filtered.pkl', 'wb') as f:
            pickle.dump(geo_filtered, f)
        print('done')
        for p in processes:
            p.kill()


