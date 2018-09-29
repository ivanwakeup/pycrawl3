import re
from urllib.parse import urlparse
import requests
import requests.exceptions
from bs4 import BeautifulSoup
from pycrawl3.utils.logger import log


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
    except requests.exceptions.RequestException as e:
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
            if not blacklist.is_blacklisted(url_extras[4]):
                links.add(link)
        else:
            links.add(link)
    log.debug("done finding links")
    return links






