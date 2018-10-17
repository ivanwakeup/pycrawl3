import django
if not hasattr(django, 'apps'):
    django.setup()

from django.conf import settings
from pycrawl3.settings import common

if not settings.configured:
    settings.configure(default_settings=common, DEBUG=True)


from pycrawl3.models import Seed
from google import google
import csv
from pycrawl3.persistence.persistence import SeedDelegate
from pycrawl3.nlp.similar_words import get_similar_words
from pycrawl3.utils.logger import log
import time, random


def load_csv_seeds(file):
    seed_package = []
    with open(file, newline='\n') as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        for row in reader:
            category = row[0]
            topic = row[1]
            search_term = row[2]
            seed_package.append((category, topic, search_term))

    for p in seed_package:
        weighted_terms = get_similar_words(p[1])

        log.info("waiting 60 seconds before making next google search....")
        time.sleep(random.randint(50,65))
        log.info("trying to search google for {}".format(p[2]))

        try:
            results = google.search(p[2], 1)
        except Exception as e:
            log.error("There was an issue searching google: {}".format(e))
            continue

        for result in results:
            seed = Seed(
                url=result.link,
                category=p[0],
                search_term=p[2],
                weighted_terms=weighted_terms,
                crawled=False
            )
            SeedDelegate.add_seed_or_pass(seed)


if __name__ == "__main__":
    import sys
    cf = sys.argv[1]
    load_csv_seeds(cf)