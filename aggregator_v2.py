import os
import pickle
import json
import queue
import threading
import pycountry


def filter_info(old):
    new = {
        'created_at': old['created_at'],
        'id': old['id'],
        'text': old['text'],
        'source': old['source'],
        'translated_text': old['translated_text'],
        'country_code': old['place']['country_code']
    }
    return new


def file_processor():
    while True:
        file_path = q.get()
        with open(file_path) as f:
            for line in f:
                tweet = filter_info(json.loads(line))
                country = tweet['country_code']
                if country == '':
                    continue
                if country not in country_tweets:
                    country_tweets[country] = list()
                tweets = country_tweets[country]
                tweets.append(tweet)
        processed_names.add(file_path)
        q.task_done()


if __name__ == '__main__':
    q = queue.Queue()
    for i in range(20):
        threading.Thread(target=file_processor, daemon=True).start()
    try:
        with open('aggregated.pkl', 'rb') as pf:
            processed_names = pickle.load(pf)
    except FileNotFoundError:
        processed_names = set()
    country_tweets = {}
    for path, dirs, files in os.walk('processed'):
        for file in files:
            file_path = os.path.join(path, file)
            if file_path in processed_names or not file.endswith('.json'):
                continue
            q.put(file_path)

    q.join()
    with open('aggregated.pkl', 'wb') as pf:
        pickle.dump(processed_names, pf)
    for country, tweets in country_tweets.items():
        with open(os.path.join('countries', country + '.json'), 'a') as f:
            for tweet in tweets:
                f.write(json.dumps(tweet) + '\n')
