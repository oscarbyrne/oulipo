import random
import logging
import re

from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers

from ..paid import Langdetecter


#TO DO:
#   > replace str.replace for removing punctuation with a re.sub that hits all non-standard ones
#   > count whitespace and reject prose if there is too much by proportion
#   > count uppercase characters and reject prose if there are too many by proportion

class ProseFinder(object):

    @staticmethod
    def get_raw_book():
        while True:
            try:
                text = load_etext(random.randrange(46000)) #46000 is approximately size of gutenberg catalogue
            except ValueError: #in case of no download method for that text id
                pass
            else:
                return strip_headers(text)

    @classmethod
    def get_raw_paragraph(cls):
        text = cls.get_raw_book()
        paragraphs = text.split("\n\n")
        return paragraphs[len(paragraphs)//2]

    @staticmethod
    def is_useful_prose(text):
        suitable_length = len(text) > 300 and len(text) < 2000
        if not suitable_length:
            return False

        is_english = Langdetecter().is_english(text.split(".")[0]) #check first sentence
        if not is_english:
            return False

        return True

    @staticmethod
    def sanitize_text(text):
        text = text.replace("_", "").replace("*", "")   #remove non-standard punctuation
        text = re.sub("\[[^\]]*\] ", "", text)          #remove text contained in square brackets
        text = " ".join(text.split())                   #remove unnecessary whitespace
        return text

    @classmethod
    def get_paragraph(cls):
        while True:
            paragraph = cls.get_raw_paragraph()
            if cls.is_useful_prose(paragraph):
                return cls.sanitize_text(paragraph)
            else:
                pass
