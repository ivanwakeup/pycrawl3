from collections import deque

from django.shortcuts import render

from pycrawl3.crawler import crawler
from pycrawl3.crawler.blacklist import Blacklist
from pycrawl3.writer.writer import PostgresWriter, EmailDelegate


def index(request):
    return render(request, 'pycrawl3/index.html')


def crawl(request):
    if request.method == 'POST':
        urls = request.POST.get('urls')
        start_crawls(urls)

    return render(request, 'pycrawl3/index.html')


def start_crawls(urls):
    url_blacklist = Blacklist.factory("url")
    email_blacklist = Blacklist.factory("email")
    writer = PostgresWriter()
    delegate = EmailDelegate(writer, email_blacklist)
    for url in urls:
        q = deque()
        q.append(url)
        c = crawler.EmailCrawler(q, url_blacklist, delegate)
        c.start()
