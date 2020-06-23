import json
import progressbar

if __name__ == '__main__':
    with open('all.json') as f:
        tweets = json.load(f)
    with open('sentiments.json') as f:
        sentiments = json.load(f)
    for i in progressbar.progressbar(range(len(tweets))):
        tweets[i]['sentiment'] = sentiments[i]
    with open('all_with_sentiments.json', 'w') as f:
        json.dump(tweets, f)
