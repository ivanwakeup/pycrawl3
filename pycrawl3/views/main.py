from django.shortcuts import render


def index(request):
    return render(request, 'pycrawl3/index.html')


def crawl(request):
    return render(request, 'pycrawl3/index.html')