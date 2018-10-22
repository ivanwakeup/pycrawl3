import sys
import os
sys.path.append(os.environ.get("PYCRAWL3_HOME"))

import django
if not hasattr(django, 'apps'):
    django.setup()

from django.conf import settings
from pycrawl3.settings import common

if not settings.configured:
    settings.configure(default_settings=common, DEBUG=True)

from pycrawl3.models import PotentialBlogger
from pycrawl3.crawler.analyzer import BloggerDomainAnalyzer
from pycrawl3.crawler.crawler import BloggerDomainCrawler
from multiprocessing import Pool
from pycrawl3.crawler.scoring import score_blogger


def mp_handler(bloggers):
    p = Pool(8)
    try:
        p.map(dispatch_analyzer, bloggers)
    except:
        pass

def dispatch_analyzer(blogger):
    analyzer = BloggerDomainAnalyzer(blogger.domain)
    crawler = BloggerDomainCrawler(blogger, analyzer, limit=10)
    blogger_updated = crawler.start()
    blogger_updated.creator_score = score_blogger(blogger_updated)
    blogger_updated.save()

bloggers = PotentialBlogger.objects.distinct('email_address')

mp_handler(bloggers)

