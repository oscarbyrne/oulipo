import requests
import random
import string

from apis.free import Spellchecker


class Morpher(object):

	def __init__(self, seed):
		self.used = []
		self.word = seed

	@property
	def word(self):
		return self._word

	@word.setter
	def word(self, new):
		self.used.append(new)
		self._word = new

	@staticmethod
	def morph_word(word):
		word = list(word) #allow item assignment
		offset = random.randrange(len(word))
		word[offset] = random.choice(string.ascii_lowercase)
		return "".join(word)

	@staticmethod
	def get_spelling_suggestions(word):
		return Spellchecker().suggestions(word)

	def choose_word(self, suggested):
		choices = [word for word in suggested if word not in self.used]
		choices = [word for word in choices if all(char in string.ascii_lowercase for char in word)]
		return random.choice(choices) #will raise IndexError if unused is empty

	def iterate_word(self):
		morphed   = self.morph_word(self.word)
		suggested = self.get_spelling_suggestions(morphed)
		try:
			self.word = self.choose_word(suggested)
		except IndexError: #all suggested words have been used
			raise StopIteration

	def __iter__(self):
		return self

	def next(self):
		self.iterate_word()
		return self.word



if __name__ == "__main__":
	random.seed()
	while True:
		morpher = Morpher("funk")
		print "funk"
		for word in morpher:
			print word


