from django.shortcuts import render

from pycrawl3.crawler import crawler
from pycrawl3.crawler.blacklist import Blacklist
from pycrawl3.writer.writer import PostgresWriter, EmailDelegate, SeedDelegate

from multiprocessing import Pool


def index(request):
    return render(request, 'pycrawl3/index.html')


def crawl(request):
    if request.method == 'POST':
        urls = request.POST.get('urls')
        url_list = urls.split('\r\n')
        mp_crawl_handler(url_list)

    return render(request, 'pycrawl3/index.html')


def add_seed_url(request):
    if request.method == 'POST':
        seeds = request.POST.get('seeds')
        seed_list = seeds.split('\r\n')
        writer = PostgresWriter(batch_size=1)
        delegate = SeedDelegate(writer)
        for seed in seed_list:
            delegate.add_seed(seed)

    return render(request, 'pycrawl3/index.html', context={'message': 'successseed'})


def start_crawls(url):
    url_blacklist = Blacklist.factory("url")
    email_blacklist = Blacklist.factory("email")
    writer = PostgresWriter(batch_size=5)
    delegate = EmailDelegate(writer, email_blacklist)
    c = crawler.EmailCrawler(url, url_blacklist, delegate)
    c.start()


def mp_crawl_handler(urls):
    p = Pool(4)
    p.map(start_crawls, urls)
