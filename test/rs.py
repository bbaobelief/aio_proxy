import requests

def count_words_at_url(url):
    resp = requests.get(url)
    import time
    time.sleep(1)
    return len(resp.text.split())
