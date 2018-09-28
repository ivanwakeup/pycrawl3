from ..utils.timeout import TimeoutError
from collections import deque
from pycrawl3.crawler.urls import *
from pycrawl3.crawler.analyzer import BloggerDomainAnalyzer


class CrawlerConfig(object):

    def __init__(self, limit=4, depth=4, max_emails_per_page=3):
        self.url_occurence_limit = limit
        self.crawler_depth = depth
        self.max_emails_per_page = max_emails_per_page


class EmailCrawler(object):

    def __init__(self, seed, url_blacklist, delegate, crawler_config=CrawlerConfig()):
        q = deque()
        q.append(seed)
        self.seed_url = seed
        self.url_queue = q
        self.blacklist = url_blacklist
        self.delegate = delegate
        self.config = crawler_config
        self.url_count_map = {}
        self.processed_urls = set()

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

            url_ops = UrlOps(url)
            if not self.should_process_url(url_ops.url_extras.base_url):
                continue

            if not url_ops.response or not url_ops.response.ok:
                continue

            try:
                new_emails = url_ops.find_emails()
                if len(new_emails) > self.config.max_emails_per_page:
                    continue
            except TimeoutError:
                continue

            for email in new_emails:
                self.delegate.add_email(email, url, seed=self.seed_url)

            new_links = url_ops.find_links(self.blacklist)
            for link in new_links:
                #only add link if crawler depth is low enough
                if link not in self.processed_urls and level < self.config.crawler_depth:
                    self.url_queue.appendleft((link, level+1))

        log.info("{} finished crawling".format(self.__class__.__name__ + str(id(self))))
        return


class BloggerCrawler(object):

    def __init__(self, seed, url_blacklist, delegate=None, crawler_config=CrawlerConfig(limit=10, depth=4)):
        q = deque()
        q.append(seed)
        self.seed_url = seed
        self.url_queue = q
        self.blacklist = url_blacklist
        self.delegate = delegate
        self.config = crawler_config
        self.url_count_map = {}
        self.processed_urls = set()

    def start(self):
        self.crawl()

    def should_process_domain(self, base_url):
        if not self.blacklist.is_blacklisted(base_url):
            return True
        return False

    #process URL only if base url has occurred less than or equal to configurable limit
    def should_process_url(self, base_url):
        if base_url in self.url_count_map:
            if self.url_count_map[base_url] > self.config.url_occurence_limit:
                self.url_count_map[base_url] += 1
                return False
            else:
                self.url_count_map[base_url] += 1
                return True
        else:
            if self.should_process_domain(base_url):
                self.url_count_map[base_url] = 1
                return True
        return False

    def enqueue_new_urls(self, url_extras, new_urls, level):
        for link in new_urls:
            new_extras = UrlExtras(link)
            if link not in self.processed_urls and level < self.config.crawler_depth:
                #append websites from the same domain to the start of the queue
                if self.should_process_url(url_extras.base_url):
                    if url_extras.base_url == new_extras.base_url:
                        self.url_queue.append((link, level))
                    else:
                        self.url_queue.appendleft((link, level+1))

    def crawl(self):
        analyzer = BloggerDomainAnalyzer()
        start_url = UrlExtras(self.url_queue[-1][0])

        while self.url_queue:
            url, level = self.url_queue.pop()
            # add to processed immediately, to support failure
            self.processed_urls.add(url)
            url_ops = UrlOps(url)

            #if we're done processing this domain, refresh the analyzer
            if not start_url.base_url == url_ops.url_extras.base_url:
                analyzer.flush()

            if not self.should_process_url(url_ops.url_extras.base_url):
                continue

            if not url_ops.response or not url_ops.response.ok:
                continue

            try:
                new_emails = url_ops.find_emails()
            except TimeoutError:
                continue

            analyzer.addEmails(new_emails)
            analyzer.addResponse(url_ops.response)

            new_links = url_ops.find_links()
            self.enqueue_new_urls(url_ops.url_extras, new_links, level)

        log.info("{} finished crawling".format(self.__class__.__name__ + str(id(self))))
        return 0
