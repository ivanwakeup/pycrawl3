from collections import deque

from django.shortcuts import render

from pycrawl3.crawler import crawler
from pycrawl3.crawler.blacklist import Blacklist
from pycrawl3.writer.writer import PostgresWriter, EmailDelegate


def index(request):
    return render(request, 'pycrawl3/index.html')


def crawl(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        queue = deque()
        queue.append(url)
        url_blacklist = Blacklist.factory("url")
        email_blacklist = Blacklist.factory("email")
        writer = PostgresWriter()
        delegate = EmailDelegate(writer, email_blacklist)
        crawler \
            .EmailCrawler(queue, url_blacklist, delegate) \
            .start()

    return render(request, 'pycrawl3/index.html')
