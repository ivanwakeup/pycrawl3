from django.shortcuts import render
from pycrawl3.crawler import crawler

def index(request):
    return render(request, 'pycrawl3/index.html')


def crawl(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        crawler.crawl_from_url(url)

    return render(request, 'pycrawl3/index.html')