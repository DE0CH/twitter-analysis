import googletrans
import json
import traceback
import os
import bz2
if __name__ == '__main__':
    translator = googletrans.Translator()
    with open('processed/all.json', 'w') as out_file:
        for path, dirs, files in os.walk('downloads'):
            if not dirs:
                for file_name in files:
                    with open(os.path.join(path, file_name), 'rb') as file:
                        print(os.path.join(path, file_name))
                        decompressed_string = bz2.decompress(file.read())
                        lines = decompressed_string.decode('utf-8').split('\n')
                        for line in lines:
                            # noinspection PyBroadException
                            try:
                                twit = json.loads(line)
                                try:
                                    if twit["geo"] is not None:
                                        twit["translated_text"] = translator.translate(twit['text'], dest='en').text
                                        out_s = json.dumps(twit) + '\n'
                                        out_file.write(out_s)
                                except KeyError:
                                    pass
                            except:
                                pass


