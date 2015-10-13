from .common import PaidAPI


class Classifier(PaidAPI):

    name = "virtan-nlp-tools-v1"
    free_requests = 20000

    classifications = [
        "adjective",
        "adverb",
        "basic_emotion",
        "connective",
        "html_tag",
        "noun",
        "number",
        "persuasive",
        "tag",
        "verb"
    ]

    def word_is(self, classification, word):
        if classification not in self.classifications:
            raise SyntaxError("Classification '{}' not supported".format(classification))
        else:
            return self.get("is/{}".format(classification), params={"q": word})["ok"]

    def classify(self, word):
        return {classification: word_is(classification, word) for classification in self.classifications}
