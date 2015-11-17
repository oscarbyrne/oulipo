from .common import get


api_name = "loudelement-free-natural-language-processing-service"

def language(text):
    r = get(api_name, "nlp-text", params={"text": text})
    return r["language"]

def is_english(text):
    return language(text) == "english"

def sentiment(text):
    r = get(api_name, "nlp-text", params={"text": text})
    return r["sentiment-score"]
