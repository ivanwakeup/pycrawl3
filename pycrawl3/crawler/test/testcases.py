import unittest
from pycrawl3.crawler.analyzer import TagScrubber


class TestCrawler(unittest.TestCase):

    def test_tag_scrubber(self):
        scrubber = TagScrubber()
        words = scrubber.filter_words
        phrases = scrubber.filter_phrases

        self.assertTrue(scrubber.filterwords(words, ['contact mario']) == ['mario'])
        self.assertTrue(scrubber.filterphrases(phrases, ['php include_once']) == [])

        self.assertTrue(scrubber.is_foreign_language(['augusztus', 'hímzett', 'megosztás', 'július',
                                             'március', 'február', 'október', 'szeptember', 'április', 'május']))