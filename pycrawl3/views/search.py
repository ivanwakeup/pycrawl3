from google import google
from django.shortcuts import render
from pycrawl3.persistence.persistence import PostgresWriter, SeedDelegate


def search_google(request):
    if request.method == "POST":
        term = request.POST.get("search-term")
        search_results = google.search(term, 1)

        writer = PostgresWriter(batch_size=1)
        delegate = SeedDelegate(writer)

        for result in search_results:
            delegate.add_seed(result.link)

        return render(request, 'pycrawl3/index.html', context={'message': 'successseed'})