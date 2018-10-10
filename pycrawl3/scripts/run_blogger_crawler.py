import django
django.setup()

import sys
from pycrawl3.settings.common import BASE_DIR
from blacklist import FileBlacklist
from pycrawl3.crawler.crawler import BloggerCrawler
from pycrawl3.persistence.persistence import PostgresWriter, BloggerDelegate


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("wrong args supplied")
        sys.exit(1)
    url = sys.argv[1]
    bl_file = BASE_DIR + "/static/pycrawl3/top_sites.txt"

    writer = PostgresWriter(batch_size=1)
    delegate = BloggerDelegate(writer, None)

    blacklist = FileBlacklist(bl_file)
    c = BloggerCrawler((url, 1), blacklist, delegate=delegate)
    c.start()