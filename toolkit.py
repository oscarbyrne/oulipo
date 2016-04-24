import random
import string

import numpy as np

import apis
import nlp

random.seed()


def ensure_unicode(string):
    if isinstance(string, str):
        return string.decode('utf-8')
    else:
        return string

def mutate(word):
    word = list(word) #allow item assignment
    offset = random.randrange(len(word))
    word[offset] = random.choice(string.ascii_lowercase)
    return "".join(word)

def contains_only_letters(word):
    return all(char in string.ascii_lowercase for char in word.lower())

def clinamens(word):
    mutated = mutate(word)
    suggestions = apis.spellcheck.suggestions(mutated)
    return [word for word in suggestions if contains_only_letters(word)]

def lexemes_ranked_by_similarity_to(token):
    excluded = [token.lemma_.lower(), token.lower_]
    not_this = np.vectorize(lambda lexeme: lexeme.lower_ not in excluded)
    words = nlp.unique_words[not_this(nlp.unique_words)]
    similarity = np.vectorize(token.similarity)
    return words[np.argsort(similarity(words))][::-1]
