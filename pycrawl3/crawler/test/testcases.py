import unittest
from pycrawl3.crawler.analyzer import TagScrubber, BloggerDomainAnalyzer
from pycrawl3.crawler.crawler import BloggerDomainCrawler


class TestCrawler(unittest.TestCase):

    def test_tag_scrubber(self):
        scrubber = TagScrubber()
        words = scrubber.filter_words
        phrases = scrubber.filter_phrases

        self.assertTrue(scrubber.filterwords(words, ['contact mario']) == ['mario'])
        self.assertTrue(scrubber.filterphrases(phrases, ['php include_once']) == [])

        self.assertTrue(scrubber.is_foreign_language(['augusztus', 'hímzett', 'megosztás', 'július',
                                             'március', 'február', 'október', 'szeptember', 'április', 'május']))

    def test_blogger_domain_analyzer(self):
        analyzer = BloggerDomainAnalyzer()
        url = "http://www.restaurantauctionslist.com"
        crawler = BloggerDomainCrawler(url, analyzer)
        data = crawler.start()
        print(data)