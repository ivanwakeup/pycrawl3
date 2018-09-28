import re
from urllib.parse import urlparse
import requests
import requests.exceptions
from bs4 import BeautifulSoup
from pycrawl3.utils.logger import log


class UrlExtras(object):
    url = None
    base_url = None
    base_url_no_scheme = None
    path = None
    response = None

    def __init__(self, url):
        self.url = url
        self.__init_url_extras(url)

    def __init_url_extras(self, url):
        parts = urlparse(url)
        try:
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            no_scheme = parts[1]
        except UnicodeEncodeError:
            base_url = None
            no_scheme = None
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url
        self.base_url = base_url
        self.path = path
        self.base_url_no_scheme = no_scheme

    @staticmethod
    def get_base_url(url):
        parts = urlparse(url)
        try:
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            no_scheme = parts[1]
        except UnicodeEncodeError:
            base_url = None



class UrlOps(object):
    url_extras = None
    response = None

    def __init__(self, url):
        self.url = url
        self.url_extras = UrlExtras(url)
        self.__init__url_response(url)

    def __init__url_response(self, url):
        log.info("Processing %s" % url)
        try:
            response = requests.get(url, timeout=3)
        except requests.exceptions.RequestException as e:
            log.debug("{} failed: {}".format(url, str(e)))
            response = None
            log.debug("done processing")
        self.response = response

    def find_emails(self):
        emails = set(re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", self.response.text, re.I))
        return emails

    def find_links(self, blacklist=None):
        log.debug("Creating BeautifulSoup for %s" % self.url_extras.base_url)
        soup = BeautifulSoup(self.response.text, "html.parser")
        links = set()
        # find and process all the anchors in the document
        for anchor in soup.find_all("a"):
            # extract link url from the anchor
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            # resolve relative links
            if link.startswith('/'):
                link = self.url_extras.base_url + link
            elif not link.startswith('http'):
                link = self.url_extras.path + link

            if blacklist:
                if not blacklist.is_blacklisted(link):
                    links.add(link)
            else:
                links.add(link)
        log.debug("done finding links")
        return links



