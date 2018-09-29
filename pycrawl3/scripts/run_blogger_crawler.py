import sys
from pycrawl3.settings.common import BASE_DIR
from pycrawl3.emails.blacklist import FileBlacklist
from pycrawl3.crawler.crawler import BloggerCrawler


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("wrong args supplied")
        sys.exit(1)
    url = sys.argv[1]
    bl_file = BASE_DIR + "/../static/pycrawl3/top_sites.txt"
    blacklist = FileBlacklist(bl_file)
    c = BloggerCrawler((url, 1), blacklist)
    c.start()