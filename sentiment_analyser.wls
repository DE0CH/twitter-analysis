#!/usr/bin/env wolframscript
tweets = Import["all.json", "RawJSON"];
getSentiment := Classify["Sentiment", #[["text"]], "Probabilities"] &;
sentiments = getSentiment /@ tweets;
Export["sentiments.json", sentiments];
