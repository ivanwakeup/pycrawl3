from collections import deque

from django.shortcuts import render

from pycrawl3.crawler import test
from pycrawl3.crawler.blacklist import Blacklist
from pycrawl3.writer.writer import PostgresWriter, EmailDelegate


def index(request):
    return render(request, 'pycrawl3/index.html')


def crawl(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        queue = deque(url)
        url_blacklist = Blacklist.factory("url")
        email_blacklist = Blacklist.factory("email")
        writer = PostgresWriter()
        delegate = EmailDelegate(writer, email_blacklist)
        crawler = test.EmailCrawler(queue, url_blacklist, delegate)
        crawler.start()

    return render(request, 'pycrawl3/index.html')
