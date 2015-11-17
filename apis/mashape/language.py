import requests

from ..keys import mashape_key, lang_detect_key


headers = {
    "X-Mashape-Key": mashape_key,
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
}

url = "https://community-language-detection.p.mashape.com/detect"

def detect(text):
    r = requests.post(url, headers=headers, params={"key": lang_detect_key, "q": text}).json()
    most_reliable = sorted(r["data"]["detections"], key=lambda k: k["confidence"])[0]
    if most_reliable["isReliable"]:
        return most_reliable["language"]
    else:
        return None

def is_english(text):
    return detect(text) == "en"
