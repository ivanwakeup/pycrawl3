import sys
sys.path.append('/home/ivanwakeup/projects/pycrawl3')

import django
if not hasattr(django, 'apps'):
    django.setup()

from django.conf import settings
from pycrawl3.settings import common

if not settings.configured:
    settings.configure(default_settings=common, DEBUG=True)

from pycrawl3.models import Seed
import multiprocessing
from pycrawl3.crawler.blacklist import Blacklist
from pycrawl3.utils.logger import log
from pycrawl3.settings.common import BASE_DIR
from pycrawl3.emails.emails import EmailRanker
from pycrawl3.crawler.crawler import PotentialBloggerCrawler


def start_blogger_crawl():
    seeds = Seed.objects.filter(crawled=False).order_by('?')
    log.info("got {} seeds, setting up crawl package".format(len(seeds)))

    base = BASE_DIR + '/dictionaries/'
    ranker = EmailRanker(base+'sales_words.txt', base+'common_names_sorted.txt', base+'top_sites.txt')

    # initialize crawl package
    crawl_package = []
    url_blacklist = Blacklist.factory("file", file=base+"top_sites.txt")
    email_blacklist = Blacklist.factory("emails")
    for seed in seeds:
        crawl_package.append((seed, url_blacklist, email_blacklist, ranker))
    mp_blogger_handler(crawl_package)


def mp_blogger_handler(crawl_package):
    p = multiprocessing.Pool(8)
    try:
        log.debug("starting new thread {} for crawler...".format(multiprocessing.current_process()))
        p.map(dispatch_blogger_crawlers, crawl_package)
    except Exception as e:
        log.error("{} exception thrown in mp_blogger_handler....continuing anyway.".format(e))
        pass


def dispatch_blogger_crawlers(crawl_package):
    seed, url_blacklist, email_blacklist, email_ranker = crawl_package
    c = PotentialBloggerCrawler(seed, url_blacklist)
    c.start()


if __name__ == "__main__":
    start_blogger_crawl()
