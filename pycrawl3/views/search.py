from google import google
from django.shortcuts import render
from pycrawl3.models import Seed
from pycrawl3.persistence.persistence import SeedDelegate


def search_google(request):
    if request.method == "POST":
        term = request.POST.get("search-term")
        weights = request.POST.get("weighted-terms", None)
        search_results = google.search(term, 1)

        for result in search_results:
            seed = Seed(
                url=result.link,
                search_term=term,
                weighted_terms=weights,
                crawled=False
            )
            SeedDelegate.add_or_update_seed(seed)

        return render(request, 'pycrawl3/index.html', context={'message': 'successseed'})


