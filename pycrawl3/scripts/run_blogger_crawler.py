import django
django.setup()

import sys
from pycrawl3.settings.common import BASE_DIR
from pycrawl3.crawler.blacklist import FileBlacklist
from pycrawl3.crawler.crawler import PotentialBloggerCrawler
from pycrawl3.persistence.persistence import PostgresWriter, BloggerDelegate
from pycrawl3.models import Seed


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("wrong args supplied")
        sys.exit(1)
    url = sys.argv[1]
    bl_file = BASE_DIR + "/dictionaries/top_sites.txt"

    writer = PostgresWriter(batch_size=1)
    delegate = BloggerDelegate(writer, None)

    seed = Seed(
        url=url,
        search_term="script",
        crawled=False
    )
    blacklist = FileBlacklist(bl_file)
    c = PotentialBloggerCrawler(seed, blacklist, delegate=delegate)
    c.start()