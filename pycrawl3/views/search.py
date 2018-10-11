from google import google
from django.shortcuts import render
from pycrawl3.models import Seed
from pycrawl3.utils.logger import log


def search_google(request):
    if request.method == "POST":
        term = request.POST.get("search-term")
        search_results = google.search(term, 1)

        for result in search_results:
            seed = Seed(
                url=result.link,
                search_term=term,
                crawled=False
            )
            log.info("writing new seed: {} to db".format(seed.url))
            seed.save()

        return render(request, 'pycrawl3/index.html', context={'message': 'successseed'})