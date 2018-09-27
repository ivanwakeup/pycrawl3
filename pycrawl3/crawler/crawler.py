import requests.exceptions
from ..utils.timeout import TimeoutError
from collections import deque
from pycrawl3.crawler.urls import *


class EmailCrawlerConfig(object):

    url_occurence_limit = None
    crawler_depth = None
    max_emails_per_page = None

    def __init__(self, limit=4, depth=4, max_emails_per_page=3):
        self.url_occurence_limit = limit
        self.crawler_depth = depth
        self.max_emails_per_page = max_emails_per_page


class EmailCrawler(object):
    url_count_map = {}
    processed_urls = set()
    config = None
    seed_url = None

    def __init__(self, seed, url_blacklist, delegate, crawler_config=EmailCrawlerConfig()):
        q = deque()
        q.append(seed)
        self.seed_url = seed
        self.url_queue = q
        self.blacklist = url_blacklist
        self.delegate = delegate
        self.config = crawler_config

    def start(self):
        self.crawl()


    def scrub_visited(self, linkset, to_process, processed):
        # add the new url to the queue if it was not enqueued nor processed yet
        tmp = set()
        for link in linkset:
            if link not in to_process and link not in processed:
                tmp.add(link)
        return tmp

    #process URL only if base url has occurred less than or equal to configurable limit
    def should_process_url(self, base_url):
        if base_url in self.url_count_map:
            if self.url_count_map[base_url] >= self.config.url_occurence_limit:
                self.url_count_map[base_url] += 1
                return False
            else:
                self.url_count_map[base_url] += 1
        else:
            self.url_count_map[base_url] = 1
        return True

    def crawl(self):
        while self.url_queue:
            url, level = self.url_queue.pop()
            # add to processed immediately, to support failure
            self.processed_urls.add(url)

            url_extras = get_url_extras(url)
            if not self.should_process_url(url_extras[1]):
                continue

            response = get_url_response(url)
            if not response or not response.ok:
                continue

            try:
                new_emails = find_emails(response)
                if len(new_emails) > self.config.max_emails_per_page:
                    continue
            except TimeoutError:
                continue

            for email in new_emails:
                self.delegate.add_email(email, url, seed=self.seed_url)

            new_links = find_links(response, url_extras, self.blacklist)
            for link in new_links:
                #only add link if crawler depth is low enough
                if link not in self.processed_urls and level < self.config.crawler_depth:
                    self.url_queue.appendleft((link, level+1))

        log.info("{} finished crawling".format(self.__class__.__name__ + str(id(self))))
        return


class BloggerCrawler(object):
    url_count_map = {}
    processed_urls = set()
    config = None
    seed_url = None

    def __init__(self, seed, url_blacklist, delegate, crawler_config=EmailCrawlerConfig()):
        q = deque()
        q.append(seed)
        self.seed_url = seed
        self.url_queue = q
        self.blacklist = url_blacklist
        self.delegate = delegate
        self.config = crawler_config

    def start(self):
        self.crawl()

    #process URL only if base url has occurred less than or equal to configurable limit
    def should_process_url(self, base_url):
        if base_url in self.url_count_map:
            if self.url_count_map[base_url] >= self.config.url_occurence_limit:
                self.url_count_map[base_url] += 1
                return False
            else:
                self.url_count_map[base_url] += 1
        else:
            self.url_count_map[base_url] = 1
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
                if len(new_emails) > self.config.max_emails_per_page:
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