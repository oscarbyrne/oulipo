from .common import get


api_name = "montanaflynn-spellcheck"

def suggestions(word):
    r = get(api_name, "check", params={"text": word})
    try:
        return r["corrections"][word]
    except KeyError:
        return [r["suggestion"]]
