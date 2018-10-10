import unittest
from pycrawl3.crawler.analyzer import TagScrubber


class TestCrawler(unittest.TestCase):

    def test_tag_scrubber(self):
        scrubber = TagScrubber()
        tags = ['artist', 'workshops galleries', 'email newsletter', 'galleries events', 'mario a', 'books email', 'store workshops', 'robinson tweet', 'events mario', 'newsletter contact']
        print(scrubber.scrub_tags(tags))