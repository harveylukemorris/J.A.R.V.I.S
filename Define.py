import re
from urllib2 import Request, urlopen, URLError
import json

WORDS = ["DEFINE","WHAT DOES %S MEAN","DEFINITION", "WHAT IS [A|AN]? %S"]

PRIORITY = 1


def handle(text, mic, profile, recursive=False):
    text = re.sub(r"(?i)(define|(what is the\s)?definition of|what does|mean|what is (a|an)?)\b","", text ).strip()
    if len(text) != 0:
        #Yandex Dictionary API Key
        dict_key = profile['keys']['YANDEX_DICT']
        #method to get the def
        get_def(text,mic,dict_key)
    elif not recursive:
        mic.say("What word would you like to define?")
        handle(mic.activeListen(), mic, profile, True)


def get_def(text,mic,key):
    #make a call to the API
    request = Request('https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key='+key+'&lang=en-en&text='+text)
    try:
        response = urlopen(request)
        data = json.load(response)
        if len(data["def"]) == 0:
            mic.say("I could not find a definition for " + str(text))
        else:
            #get the word type (noun, verb, ect)
            word_type = data["def"][0]["pos"]
            mic.say("The word is a " + word_type)
            defs = data["def"][0]["tr"]
            #loop through the definitions
            for text in defs:
                mic.say(text["text"])
    except URLError, e:
        mic.say("Unable to reach dictionary API.")


def isValid(text):
    return bool(re.search(r'\Define|what does\s(.*?)\smean|Definition|what is\s\w+\b',text, re.IGNORECASE))
