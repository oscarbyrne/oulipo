from ..common import MashapeAPI


class Spellchecker(MashapeAPI):

    name = "montanaflynn-spellcheck"

    def suggestions(self, word):
        r = self.get("check", params={"text": word})
        try:
            return r["corrections"][word]
        except KeyError:
            return [r["suggestion"]]