import requests, uuid, json
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

def getMultipleTranslations(word,from_,to,key):
    translations = microsoftDictionaryLookup(word,from_,to,key)
    #print(translations)
    translations = [trans["displayTarget"] for trans in translations]
    return translations