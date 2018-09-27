import re

import requests
import requests.exceptions
from bs4 import BeautifulSoup
from bs4.element import Comment
from collections import Counter


from pycrawl3.utils.logger import log


def get_url_response(url):
    log.info("Fetching url: %s" % url)
    try:
        response = requests.get(url, timeout=3)
    except requests.exceptions.RequestException as e:
        log.debug("{} failed: {}".format(url, str(e)))
        response = None
        log.debug("done processing")
    return response


def get_words_from_text(text_string, minimum_count=3):
    lst = re.findall(r'\b\w+', text_string)
    lst = [x.lower() for x in lst]
    counter = Counter(lst)
    occs = [(word, count) for word, count in counter.items() if count > minimum_count]
    return occs


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def get_visible_text(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def filter_stop_words(text_string):
    return re.findall(r'^/\b([a-z0-9]+)\b(?<!ignoreme|ignoreme2|ignoreme3)')





