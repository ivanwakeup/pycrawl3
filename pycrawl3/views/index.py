from django.shortcuts import render
from django.http import HttpResponse

from pycrawl3.crawler import crawler
from pycrawl3.crawler.blacklist import Blacklist
from pycrawl3.persistence.persistence import PostgresWriter, EmailDelegate, SeedDelegate, BloggerDelegate

from multiprocessing import Pool
from ..resources import EmailResource
from pycrawl3.emails.emails import EmailRanker

from pycrawl3.settings.common import BASE_DIR
from pycrawl3.models import Seed

from random import shuffle

base_template = 'pycrawl3/index.html'


def index(request):
    return render(request, base_template)


def crawl(request):
    if request.method == 'POST':
        urls = request.POST.get('urls')
        url_list = urls.split('\r\n')
        url_tuple = [(url, 1) for url in url_list]
        mp_crawl_handler(url_tuple)

    return render(request, base_template)


def start_crawl(request):
    seeds = Seed.objects.filter(crawled=False).order_by('?')

    #initialize crawl package
    crawl_package = []
    url_blacklist = Blacklist.factory("url")
    email_blacklist = Blacklist.factory("emails")

    base = BASE_DIR + '/dictionaries/'
    ranker = EmailRanker(base+'sales_words.txt', base+'common_names_sorted.txt', base+'top_sites.txt')
    for seed in seeds:
        seed.crawled = True
        seed.save()
        crawl_package.append((seed, url_blacklist, email_blacklist, ranker))
    mp_crawl_handler(crawl_package)

    return render(request, base_template)


def start_blogger_crawl(request):
    seeds = Seed.objects.filter(crawled=False).order_by('?')
    print(len(seeds))
    base = BASE_DIR + '/dictionaries/'
    ranker = EmailRanker(base+'sales_words.txt', base+'common_names_sorted.txt', base+'top_sites.txt')

    # initialize crawl package
    crawl_package = []
    url_blacklist = Blacklist.factory("file", file=base+"top_sites.txt")
    email_blacklist = Blacklist.factory("emails")
    for seed in seeds:
        crawl_package.append((seed, url_blacklist, email_blacklist, ranker))
    mp_blogger_handler(crawl_package)

    return render(request, base_template)


def add_seed_url(request):
    if request.method == 'POST':
        seeds = request.POST.get('seeds')
        seed_list = seeds.split('\r\n')
        writer = PostgresWriter(batch_size=1)
        delegate = SeedDelegate(writer)
        for seed in seed_list:
            delegate.add_seed(seed)

    return render(request, base_template)


def get_emails_as_csv(request):
    er = EmailResource()
    dataset = er.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="persons.csv"'
    return response


def dispatch_crawlers(crawl_package):
    seed, url_blacklist, email_blacklist, email_ranker = crawl_package
    writer = PostgresWriter(batch_size=1)
    delegate = EmailDelegate(writer, email_blacklist, email_ranker)
    c = crawler.EmailCrawler(seed, url_blacklist, delegate)
    c.start()


def dispatch_blogger_crawlers(crawl_package):
    seed, url_blacklist, email_blacklist, email_ranker = crawl_package
    writer = PostgresWriter(batch_size=1)
    delegate = BloggerDelegate(writer, None)
    c = crawler.BloggerCrawler(seed, url_blacklist, delegate)
    c.start()


def mp_crawl_handler(crawl_package):
    p = Pool(4)
    try:
        p.map(dispatch_crawlers, crawl_package)
    except:
        pass


def mp_blogger_handler(crawl_package):
    p = Pool(4)
    try:
        p.map(dispatch_blogger_crawlers, crawl_package)
    except:
        pass