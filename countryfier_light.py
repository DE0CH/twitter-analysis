import json
import os

if __name__ == '__main__':
    countries = {}
    with open('all_with_sentiments.json') as f:
        tweets = json.load(f)
    for tweet in tweets:
        if tweet['country_code'] not in countries:
            countries[tweet['country_code']] = []
        countries[tweet['country_code']].append(tweet)
    with open('all_by_countries.json', 'w') as f:
        json.dump(countries, f)
