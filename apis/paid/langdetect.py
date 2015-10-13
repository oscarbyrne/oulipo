from .common import PaidAPI


class Langdetecter(PaidAPI):

	name = "langdetect"
	free_requests = 2000

	def language(self, text):
		try:
			return self.get("language", params={"text": text, "mode": "json"})["lang"]
		except:
			return "unknown"

	def is_english(self, text):
		return self.language(text) == "en"