# noinspection PyPackageRequirements
import json
import os
import bz2
import multiprocessing
import coloredlogs, logging
import pickle


def worker(q, geo_filtered_dict):
    while True:
        path, file_name = q.get()
        process_files(path, file_name, geo_filtered_dict)
        q.task_done()


def process_files(path, file_name, geo_filtered_dict):
    file_name_no_extension, file_extension = os.path.splitext(file_name)
    out_file_name = os.path.join('processed', os.path.relpath(path, start='untarred'), file_name_no_extension)
    os.makedirs(os.path.dirname(out_file_name), exist_ok=True)
    with open(out_file_name, 'w') as out_file:
        with open(os.path.join(path, file_name), 'rb') as file:
            decompressed_string = bz2.decompress(file.read())
            lines = decompressed_string.decode('utf-8').split('\n')
            for line in lines:
                if not line.strip():
                    continue
                tweet = json.loads(line)
                try:
                    if tweet['place']['country_code']:
                        out_file.write(line)
                except KeyError:
                    pass
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
    for path, dirs, files in os.walk('untarred'):
        for file_name in files:
            if not os.path.join(path, file_name) in geo_filtered_dict and file_name.endswith('.json.bz2'):
                q.put((path, file_name))
    q.join()
    geo_filtered = set(geo_filtered_dict.keys())
    with open('geo_filtered.pkl', 'wb') as f:
        pickle.dump(geo_filtered, f)
    print('done, safe to ctrl-c if it does not exit automatically')
    for p in processes:
        p.terminate()
