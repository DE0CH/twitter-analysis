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
    out_file_name = os.path.join('en_filtered', os.path.relpath(path, start='processed'), file_name)
    os.makedirs(os.path.dirname(out_file_name), exist_ok=True)
    with open(out_file_name, 'w') as out_file:
        with open(os.path.join(path, file_name)) as file:
            tweets = json.loads(file.read())
            new_tweets = []
            for tweet in tweets:
                try:
                    if tweet.get('lang', 'en'):
                        new_tweets.append(tweet)
                except Exception as e:
                    logging.exception(e)
        out_file.write(json.dumps(new_tweets))
        logging.info('finished ' + os.path.join(path, file_name))


if __name__ == '__main__':
    coloredlogs.install()
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    q = multiprocessing.JoinableQueue()
    for i in range(os.cpu_count() - 1):
        p = multiprocessing.Process(target=worker, args=(q, ), daemon=True)
        p.start()
    for path, dirs, files in os.walk('processed'):
        for file_name in files:
            if file_name.endswith('.json'):
                q.put((path, file_name))
    q.join()
    print('done, safe to ctrl-c if it does not exit automatically')