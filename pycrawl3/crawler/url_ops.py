import re
from urllib.parse import urlparse
import requests
import requests.exceptions
from bs4 import BeautifulSoup
from pycrawl3.utils.logger import log
from bs4.element import Comment
from collections import Counter


def get_url_extras(url):
    parts = urlparse(url)
    try:
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        no_scheme = parts[1]
        no_www = no_scheme.strip('www.')
    except UnicodeEncodeError:
        base_url = None
        no_scheme = None
        no_www = None
    path = url[:url.rfind('/') + 1] if '/' in parts.path else url
    return url, base_url, path, no_scheme, no_www


def get_url_response(url):
    log.info("Processing %s" % url)
    try:
        response = requests.get(url, timeout=3)
    except (requests.exceptions.RequestException, UnicodeError) as e:
        log.debug("{} failed: {}".format(url, str(e)))
        response = None
        log.debug("done processing")
    return response


def find_emails(text):
    emails = set(re.findall(
        r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", text, re.I))
    return emails


def find_links(text, url_extras, blacklist=None):
    soup = BeautifulSoup(text, "html.parser")
    links = set()
    # find and process all the anchors in the document
    for anchor in soup.find_all("a"):
        # extract link url from the anchor
        link = anchor.attrs["href"] if "href" in anchor.attrs else ''
        # resolve relative links
        if link.startswith('/'):
            link = url_extras[1] + link
        elif not link.startswith('http'):
            link = url_extras[2] + link
        if blacklist:
            new_url_extras = get_url_extras(link)
            if not blacklist.is_blacklisted(new_url_extras[4]):
                links.add(link)
        else:
            links.add(link)
    log.debug("done finding links")
    return links


def get_visible_text(body):
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(str(t.strip()) for t in visible_texts)


def get_word_list(text_string):
    lst = re.findall(r'\b\w+', text_string)
    lst = [x.lower() for x in lst]
    return lst


def get_word_count(word_list, minimum_count=0):
    counter = Counter(word_list)
    occs = [(word, count) for word, count in counter.items() if count > minimum_count]
    return occs


def contains_stop_word(word):
    stop_words = "a|an|and|are|as|at|be|by|for|from|has|he|in|is|it|its|of|on|that|the|to|was|were|will|with"
    stop_set = set(stop_words.split("|"))
    if word in stop_set:
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
        if word.isdigit() or contains_month(word):
            continue
        result.append(word)
    return result




