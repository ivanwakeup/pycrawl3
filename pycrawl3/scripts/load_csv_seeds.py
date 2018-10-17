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


def load_csv_seeds(file):
    with open(file, newline='\n') as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        for row in reader:
            category = row[0]
            topic = row[1]
            search_term = row[2]

            weighted_terms = get_similar_words(topic)

            results = google.search(search_term, 1)
            for result in results:
                seed = Seed(
                    url=result.link,
                    category=category,
                    search_term=search_term,
                    weighted_terms=weighted_terms,
                    crawled=False
                )
                SeedDelegate.add_or_update_seed(seed)


if __name__ == "__main__":
    import sys
    cf = sys.argv[1]
    load_csv_seeds(cf)