# noinspection PyPackageRequirements
from google.cloud import translate_v2 as translate
import json
import os
import bz2
import threading
import coloredlogs, logging
import queue
import pickle


def worker():
    while True:
        path, dirs, files = q.get()
        process_files(path, dirs, files)
        q.task_done()


def process_files(path, dirs, files):
    for file_name in files:
        if os.path.join(path, file_name) in geo_filtered:
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
                        # noinspection PyBroadException
                        try:
                            if not line.strip():
                                continue
                            twit = json.loads(line)
                            if twit.get('place', None) is not None:
                                try:
                                    twit["place"]["country_code"]
                                except KeyError:
                                    logging.info(print(json.dumps(twit)))
                                if twit.get('lang', '') == 'en':
                                    twit["translated_text"] = twit['text']
                                else:
                                    twit["translated_text"] = translator.translate(
                                        twit['text'],
                                        target_language='en')['translatedText']
                                out_s = json.dumps(twit) + '\n'
                                out_file.write(out_s)
                        except Exception:
                            logging.exception('failed to process tweet')
                logging.info('finished ' + os.path.join(path, file_name))
        geo_filtered.add(os.path.join(path, file_name))


if __name__ == '__main__':
    try:
        with open('geo_filtered.pkl', 'rb') as f:
            geo_filtered = pickle.load(f)
    except FileNotFoundError:
        geo_filtered = set()
    coloredlogs.install()
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    q = queue.Queue()
    try:
        os.makedirs('processed')
    except FileExistsError:
        pass
    for i in range(10):
        t = threading.Thread(target=worker, daemon=True).start()
    total_num = 0
    filtered_num = 0
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'twitter-sentiment-analysis-f22ce784b0a8.json'
    translator = translate.Client()
    for path, dirs, files in os.walk('untarred'):
        q.put((path, dirs, files))

    q.join()
    with open('geo_filtered.pkl', 'wb') as f:
        pickle.dump(geo_filtered, f)
    print('done')
