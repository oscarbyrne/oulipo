from .common import get


api_name = "montanaflynn-dictionary"

def define(word):
    r = get(api_name, "define", params={"word": word})
    return r["definitions"][0]["text"]
