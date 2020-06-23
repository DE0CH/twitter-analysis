import re
import json
import progressbar

def filter_text(s):
    # delete all the emoji (and any non ascii characters)
    s = re.sub(r'[^\x00-\x7F]', '', s)
    # remove all the @
    s = re.sub(r'@[^\s]+', '', s)
    # remove all the #
    s = re.sub(r'#[^\s]+', '', s)
    # remove all the links
    s = re.sub(r'https://[^s]+', '', s)
    s = re.sub(r'http://[^s]+', '', s)
    return s


if __name__ == '__main__':

    with open('all.json') as f:
        tweets = json.load(f)
    with progressbar.ProgressBar(max_value=len(tweets)) as bar:
        for i, tweet in enumerate(tweets):
            tweet['text'] = filter_text(tweet['text'])
            bar.update(i)
    with open('all_text_filtered.json', 'w') as f:
        json.dump(tweets, f)
