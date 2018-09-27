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


def get_word_list(text_string):
    lst = re.findall(r'\b\w+', text_string)
    lst = [x.lower() for x in lst]
    return lst


def get_word_count(word_list, minimum_count=0):
    counter = Counter(word_list)
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
    return u" ".join(str(t.strip()) for t in visible_texts)


def contains_stop_word(word):
    stop_words = "a|an|and|are|as|at|be|by|for|from|has|he|in|is|it|its|of|on|that|the|to|was|were|will|with"
    stop_set = set(stop_words.split("|"))
    if word in stop_set:
        return True
    return False


def contains_short_word(word, length=2):
    if len(word) <= length:
        return True
    return False


def contains_month(word):
    months = set(["january", "february", "march", "april", "may", "june", "july",
                  "august", "september", "october", "november", "december"])
    if word in months:
        return True
    return False


def filter_words(word_list):
    result = []
    for word in word_list:
        if contains_stop_word(word) or contains_short_word(word) or word.isdigit() or contains_month(word):
            continue
        result.append(word)
    return result






