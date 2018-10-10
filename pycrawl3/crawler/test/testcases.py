import unittest
from pycrawl3.crawler.analyzer import TagScrubber


class TestCrawler(unittest.TestCase):

    def test_tag_scrubber(self):
        scrubber = TagScrubber()
        words = scrubber.filter_words
        phrases = scrubber.filter_phrases

        assert(scrubber.filterwords(words, ['contact mario']) == ['mario'])
        assert(scrubber.filterphrases(phrases, ['php include_once']) == [])