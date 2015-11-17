import random
import string

import apis

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

def clinaments(word):
    mutated = mutate(word)
    suggestions = apis.spellcheck.suggestions(mutated)
    return [word for word in suggestions if contains_only_letters(word)]
