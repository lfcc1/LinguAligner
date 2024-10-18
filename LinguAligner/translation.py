import deepl
import json
from deep_translator import GoogleTranslator as GT
import sys
import requests, uuid

class GoogleTranslator:
    def __init__(self, source_lang="en", target_lang="pt-pt"):
        self
        self.auth_key = "KEY"
        self.translator_google = GT(source=source_lang, target= target_lang)


    def translate(self, text):
        trans = self.translator_google.translate(text+ " ")
        if trans:
            trans = trans.strip()
        else:
            trans = text
        return trans

class DeepLTranslator:
    def __init__(self,key, source_lang="EN", target_lang="PT-PT"):
        self.auth_key = key
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.translator = deepl.Translator(key)
        
    def translate(self, text):
        result = self.translator_deepl.translate_text(text, source_lang= self.ource_lang, target_lang= self.target_lang)
        return result.text.strip()
        


class MicrosoftTranslator:
    def __init__(self,auth_key, source_lang="en", target_lang="pt-pt"):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.auth_key = auth_key

    def DictionaryLookup(self, word):
        # Add your key and endpoint
        key = self.auth_key
        endpoint = "https://api.cognitive.microsofttranslator.com"

        # location, also known as region.
        # required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
        location = "westeurope"

        #path = '/translate?api-version=3.0'
        path = '/dictionary/lookup?api-version=3.0'
        constructed_url = endpoint + path + "&includeAlignment=true"

        params = {
            'from': self.source_lang,
            'to': self.target_lang
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
    
    def getMultipleTranslations(self, word):
        translations = self.DictionaryLookup(word)
        #print(translations)
        translations = [trans["displayTarget"] for trans in translations]
        return translations
    
    def translate(self, word):
        # Add your key and endpoint
        key = self.auth_key

        endpoint = "https://api.cognitive.microsofttranslator.com"

        # location, also known as region.
        # required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
        location = "westeurope"

        path = '/translate?api-version=3.0'
        constructed_url = endpoint + path #+ "&includeAlignment=true"

        params = {
            'from': self.source_lang,
            'to': self.target_lang
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
