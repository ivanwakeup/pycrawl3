import re
from urllib.parse import urlparse

import requests
import requests.exceptions
from bs4 import BeautifulSoup

from ..utils.logger import log
from ..utils.timeout import TimeoutError
from collections import deque


class EmailCrawlerConfig(object):

    url_occurence_limit = None
    crawler_depth = None

    def __init__(self, limit, depth):
        self.url_occurence_limit = limit
        self.crawler_depth = depth


class EmailCrawler(object):
    email_count_map = {}
    processed_urls = set()
    config = None
    seed_url = None

    def __init__(self, seed, url_blacklist, delegate, crawler_config=EmailCrawlerConfig(4, 4)):
        q = deque()
        q.append(seed)
        self.seed_url = seed
        self.url_queue = q
        self.blacklist = url_blacklist
        self.delegate = delegate
        self.config = crawler_config

    def start(self):
        self.crawl()

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

    def find_emails(self, url_response):
        emails = set(re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", url_response.text, re.I))
        return emails

    def find_links(self, html, url_extras):
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
            if not self.blacklist.is_blacklisted(link):
                links.add(link)
        log.debug("done finding links")
        return links

    def scrub_visited(self, linkset, to_process, processed):
        # add the new url to the queue if it was not enqueued nor processed yet
        tmp = set()
        for link in linkset:
            if link not in to_process and link not in processed:
                tmp.add(link)
        return tmp

    #process URL only if base url has occurred less than or equal to configurable limit
    def should_process_url(self, base_url):
        if base_url in self.email_count_map:
            if self.email_count_map[base_url] >= self.config.url_occurence_limit:
                self.email_count_map[base_url] += 1
                return False
            else:
                self.email_count_map[base_url] += 1
        else:
            self.email_count_map[base_url] = 1
        return True

    def crawl(self):
        while self.url_queue:
            url, level = self.url_queue.pop()
            # add to processed immediately, to support failure
            self.processed_urls.add(url)

            url_extras = self.get_url_extras(url)
            if not self.should_process_url(url_extras[1]):
                continue

            response = self.get_url_response(url)
            if not response or not response.ok:
                continue

            try:
                new_emails = self.find_emails(response)
                if len(new_emails) > 3:
                    continue
            except TimeoutError:
                continue

            for email in new_emails:
                self.delegate.add_email(email, url, seed=self.seed_url)

            new_links = self.find_links(response, url_extras)
            for link in new_links:
                #only add link if crawler depth is low enough
                if link not in self.processed_urls and level < self.config.crawler_depth:
                    self.url_queue.appendleft((link, level+1))

        log.info("{} finished crawling".format(self.__class__.__name__ + str(id(self))))
        return

