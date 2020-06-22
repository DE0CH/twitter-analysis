import os
import json
import multiprocessing
import coloredlogs
import logging


def filter_info(old):
    new = {
        'created_at': old['created_at'],
        'id': old['id'],
        'text': old['text'],
        'source': old['source'],
        'country_code': old['place']['country_code']
    }
    return new


def file_processor(q, all_tweets):
    while True:
        file_path = q.get()
        with open(file_path) as f:
            tweets = json.loads(f.read())
            for tweet in tweets:
                all_tweets.append(filter_info(tweet))
        logging.info('finished: ' + file_path)
        q.task_done()


if __name__ == '__main__':
    coloredlogs.install()
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    q = multiprocessing.JoinableQueue()
    manager = multiprocessing.Manager()
    tweets = manager.list()
    for i in range(os.cpu_count()-1):
        p = multiprocessing.Process(target=file_processor, args=(q, tweets), daemon=True)
        p.start()
    for path, dirs, files in os.walk('en_filtered'):
        for file in files:
            file_path = os.path.join(path, file)
            if file.endswith('.json'):
                q.put(file_path)

    with open('all.json', 'w') as f:
        json.dump(list(tweets), f)

    print('done, safe to ctrl-c if it does not exit automatically')
