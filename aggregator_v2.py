import os
import pickle
import json
import queue
import threading
import pycountry


def file_processor():
    while True:
        file_path = q.get()
        with open(file_path) as f:
            for line in f:
                tweet = json.loads(line)
                country = tweet['place']['country_code']
                if country == '':
                    continue
                if country not in country_files:
                    country_files[country] = (open(os.path.join('countries', country + '.json'), 'a'),
                                              threading.Lock())
                file, lock = country_files[country]
                with lock:
                    file.write(line)
        processed_names.add(file_path)
        q.task_done()


if __name__ == '__main__':
    q = queue.Queue()
    for i in range(100):
        threading.Thread(target=file_processor, daemon=True).start()
    try:
        with open('aggregated.pkl', 'rb') as pf:
            processed_names = pickle.load(pf)
    except FileNotFoundError:
        processed_names = set()
    country_files = {}
    for path, dirs, files in os.walk('processed'):
        for file in files:
            file_path = os.path.join(path, file)
            if file_path in processed_names or not file.endswith('.json'):
                continue
            q.put(file_path)

    q.join()
    with open('aggregated.pkl', 'wb') as pf:
        pickle.dump(processed_names, pf)
    for file, lock in country_files.values():
        with lock:
            file.close()
