import re
from collections import deque
from urllib.parse import urlparse

import requests
import requests.exceptions
from bs4 import BeautifulSoup

from .blacklist import Blacklist
from .linkscrub import scrub
from .timeout import TimeoutError
from ..writer.writer import EmailDelegate, PostgresWriter

from utils.logger import log


class EmailCrawler(object):

    def __init__(self, url_queue, url_blacklist, delegate):
        self.url_queue = url_queue
        self.blacklist = url_blacklist
        self.delegate = delegate

    def get_url_extras(self, url):
        parts = urlparse(url)
        try:
            base_url = "{0.scheme}://{0.netloc}".format(parts)
        except UnicodeEncodeError:
            base_url = None
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url
        return url, base_url, path

    def get_url_response(self, url):
        log.info("Processing %s" % url)
        try:
            response = requests.get(url, timeout=3)
        except requests.exceptions.RequestException as e:
            log.debug("{} failed: {}".format(url, str(e)))
            response = None
            log.debug("done processing")
        return response

