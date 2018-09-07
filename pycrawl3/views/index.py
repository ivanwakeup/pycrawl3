from django.shortcuts import render
from django.http import HttpResponse

from pycrawl3.crawler import crawler
from pycrawl3.emails.blacklist import Blacklist
from pycrawl3.persistence.persistence import PostgresWriter, EmailDelegate, SeedDelegate

from multiprocessing import Pool
from ..resources import EmailResource
from pycrawl3.emails.emails import EmailRanker

from pycrawl3.settings.common import BASE_DIR


def index(request):
    return render(request, 'pycrawl3/index.html')


def crawl(request):
    if request.method == 'POST':
        urls = request.POST.get('urls')
        url_list = urls.split('\r\n')
        url_tuple = [(url, 1) for url in url_list]
        mp_crawl_handler(url_tuple)

    return render(request, 'pycrawl3/index.html')


def start_crawl(request):
    seeds = SeedDelegate.get_seeds_to_crawl()

    #initialize crawl package
    crawl_package = []
    url_blacklist = Blacklist.factory("url")
    email_blacklist = Blacklist.factory("emails")

    base = BASE_DIR + '/../static/pycrawl3/'
    ranker = EmailRanker(base+'sales_words.txt', base+'common_names_sorted.txt', base+'top_sites.txt')

    for seed in seeds:
        SeedDelegate.set_crawled(seed)
        crawl_package.append(((seed.url, 1), url_blacklist, email_blacklist, ranker))
    mp_crawl_handler(crawl_package)

    return render(request, 'pycrawl3/index.html', context={'message': 'successseed'})


def add_seed_url(request):
    if request.method == 'POST':
        seeds = request.POST.get('seeds')
        seed_list = seeds.split('\r\n')
        writer = PostgresWriter(batch_size=1)
        delegate = SeedDelegate(writer)
        for seed in seed_list:
            delegate.add_seed(seed)

    return render(request, 'pycrawl3/index.html', context={'message': 'successseed'})


def get_emails_as_csv(request):
    er = EmailResource()
    dataset = er.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="persons.csv"'
    return response


def dispatch_crawlers(crawl_package):
    url, url_blacklist, email_blacklist, email_ranker = crawl_package
    writer = PostgresWriter(batch_size=1)
    delegate = EmailDelegate(writer, email_blacklist, email_ranker)
    c = crawler.EmailCrawler(url, url_blacklist, delegate)
    c.start()


def mp_crawl_handler(crawl_package):
    p = Pool(4)
    try:
        p.map(dispatch_crawlers, crawl_package)
    except:
        pass
