import deepl
import json
from deep_translator import GoogleTranslator
import sys

auth_key = "KEY"
translator_deepl = deepl.Translator(auth_key)
translator_google = GoogleTranslator(source='en', target='pt')


def translateDeepL(text):
    result = translator_deepl.translate_text(text, target_lang="PT-PT")
    return result.text.strip()


def microsoftDictionaryLookup(word,from_,to, key):
    # Add your key and endpoint
    endpoint = "https://api.cognitive.microsofttranslator.com"

    # location, also known as region.
    # required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
    location = "westeurope"

    #path = '/translate?api-version=3.0'
    path = '/dictionary/lookup?api-version=3.0'
    constructed_url = endpoint + path + "&includeAlignment=true"

    params = {
        'from': from_,
        'to': to
    }

    headers = {
    'Ocp-Apim-Subscription-Key': key,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4()),

    }

    body = [{
        'Text': word
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    return response[0]["translations"]


def translateGoogle(text):
    trans = translator_google.translate(text+ " ")
    if trans:
        trans = trans.strip()
    else:
        trans = text
    return trans


import requests, uuid
def microsoftTranslate(word):
    # Add your key and endpoint
    key = ""
    endpoint = "https://api.cognitive.microsofttranslator.com"

    # location, also known as region.
    # required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
    location = "westeurope"

    path = '/translate?api-version=3.0'
    constructed_url = endpoint + path #+ "&includeAlignment=true"

    params = {
        'from': 'en',
        'to': 'pt-pt'
    }

    headers = {
    'Ocp-Apim-Subscription-Key': key,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4()),

    }

    # You can pass more than one object in body.
    body = [{
        'Text': word
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    return response[0]["translations"][0]["text"].strip()



    #print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

def dataLoad(filename):
    f = open(filename)
    texts = json.load(f)
    f.close()
    return texts

def dataSave(filename,texts):
    with  open(filename,"w") as out_f:
        json.dump(texts,out_f,indent=4,ensure_ascii=False)


def translateACE(texts):
    for si in range(len(texts)):
        s = texts[si]
        texts[si]["sentence_pt"] = translateGoogle(s["sentence"])
        for ei, e in enumerate(s["golden-event-mentions"]):
            texts[si]["golden-event-mentions"][ei]["trigger"]["text_pt"] = translateGoogle(e["trigger"]["text"]) # change translation function
            for ai, a in enumerate(e["arguments"]):
                texts[si]["golden-event-mentions"][ei]["arguments"][ai]["text_pt"] = translateGoogle(a["text"]) # change translation function
        print(si)
    return texts


def clean(texts):
    for si in range(len(texts)):
        del texts[si]["stanford-colcc"]
        del texts[si]["pos-tags"]
        del texts[si]["lemma"]
        del texts[si]["parse"]
        del texts[si]["words"]
        del texts[si]["golden-entity-mentions"]
    return texts

def main():
    if sys.argv[1] == "-h":
        print("Usage: python3 translation.py <input_file> <output_file>")
        return
    print(len(sys.argv))
    if len(sys.argv) != 3:
        print("Usage: python3 translation.py <input_file> <output_file>")
        return
    texts = dataLoad(sys.argv[1])# "../parser/ACE_2005/ace2005-preprocessing/output/dev.json"
    texts = clean(texts)
    texts = translateACE(texts)
    dataSave(sys.argv[2],texts)
    


if __name__ == '__main__':
    main()
