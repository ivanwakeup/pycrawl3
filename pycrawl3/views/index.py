from django.shortcuts import render
from django.http import HttpResponse

from pycrawl3.crawler import crawler
from pycrawl3.crawler.blacklist import Blacklist
from pycrawl3.persistence.persistence import PostgresWriter, EmailDelegate, SeedDelegate

from multiprocessing import Pool
from ..resources import EmailResource


def index(request):
    return render(request, 'pycrawl3/index.html')


def crawl(request):
    if request.method == 'POST':
        urls = request.POST.get('urls')
        url_list = urls.split('\r\n')
        mp_crawl_handler(url_list)

    return render(request, 'pycrawl3/index.html')


def start_crawl(request):
    seeds = SeedDelegate.get_seeds_to_crawl()
    urls = []
    for seed in seeds:
        SeedDelegate.set_crawled(seed)
        urls.append(seed.url)
    mp_crawl_handler(urls)
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


def dispatch_crawlers(url):
    url_blacklist = Blacklist.factory("url")
    email_blacklist = Blacklist.factory("email")
    writer = PostgresWriter(batch_size=5)
    delegate = EmailDelegate(writer, email_blacklist)
    c = crawler.EmailCrawler(url, url_blacklist, delegate)
    c.start()


def mp_crawl_handler(urls):
    p = Pool(4)
    p.map(dispatch_crawlers, urls)
