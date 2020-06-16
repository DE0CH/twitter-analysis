import json
import googletrans

if __name__ == '__main__':
    with open('downloads/01/00/29.json') as f:
        translator = googletrans.Translator()
        for line in f:
            x = json.loads(line)
            try:
                if x["geo"] is not None:
                    print(json.dumps(x["geo"]))
                    text = x["text"]
                    translated = translator.translate(text, dest='en')
                    print(text)
                    print(translated)
            except KeyError:
                pass
    