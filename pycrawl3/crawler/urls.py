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
    except UnicodeEncodeError:
        base_url = None
    path = url[:url.rfind('/') + 1] if '/' in parts.path else url
    return url, base_url, path


def get_url_response(url):
    log.info("Processing %s" % url)
    try:
        response = requests.get(url, timeout=3)
    except requests.exceptions.RequestException as e:
        log.debug("{} failed: {}".format(url, str(e)))
        response = None
        log.debug("done processing")
    return response


def find_emails(url_response):
    emails = set(re.findall(
        r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", url_response.text, re.I))
    return emails


def find_links(html, url_extras, blacklist=None):
    # create a beautiful soup for the html document
    log.debug("Creating BeautifulSoup for %s" % url_extras[1])
    soup = BeautifulSoup(html.text, "html.parser")
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
            if not blacklist.is_blacklisted(link):
                links.add(link)
        else:
            links.add(link)
    log.debug("done finding links")
    return links