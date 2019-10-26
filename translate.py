#!/usr/bin/python3

import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("text", help="The text to translate.")
parser.add_argument("-l", "--language", metavar="L", default="en-ru", help="The translation direction. You can set it in either of the following ways: As a pair of language codes separated by a hyphen (“from”-“to”). For example, en-ru indicates translating from English to Russian. As the target language code (for example, ru). In this case, the service tries to detect the source language automatically. Default - 'en-ru'.")
parser.add_argument("-d", "--dictionary", action="store_true", help="Look up the word in the dictionary. If this is set, L may be only a pair of language codes.")
args = parser.parse_args()

if args.dictionary:
    API_KEY = 'dict.1.1.20191019T141710Z.b179e7162d85a2a0.a6d6457b71c0344ff2077ee07e1399d28c8c6746'
    url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'
else:
    API_KEY = 'trnsl.1.1.20191019T130729Z.6da3abe8466701dc.e4dc1368c88a28d9fc427ae5b8f1f65f289a84fb'
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
params = dict(key=API_KEY, text=args.text, lang=args.language)
result = requests.get(url, params)
json = result.json()
if result.status_code == 200:
    if args.dictionary:
        for dic in json['def']:
            print(dic['text'], end="")
            if 'ts' in dic:
                print(" " + dic['ts'], end="")
            print(" " + dic['pos'])
            for i, tr in enumerate(dic['tr']):
                print(str(i + 1) + ". " + tr['text'], end="")
                if 'syn' in tr:
                    for syn in tr['syn']:
                        print(", " + syn['text'], end="")
                if 'mean' in tr:
                    print("\n(", end="")
                    for j, mean in enumerate(tr['mean']):
                        if j > 0:
                            print(", ", end="")
                        print(mean['text'], end="")
                    print(")", end="")
                print("")
            print("")
                    
    else:
        print(json['text'][0])
else:
    print('Error: ' + str(result.status_code))
