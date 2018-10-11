import unittest
import django
django.setup()
from pycrawl3.crawler.analyzer import TagScrubber, BloggerDomainAnalyzer
from pycrawl3.crawler.crawler import BloggerDomainCrawler, sort_links_with_priority
from pycrawl3.models import Seed, Blogger


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
        seed = Seed(
            url="http://eatingmywaythroughoc.blogspot.com/",
            search_term="testcase",
            weighted_terms="sandwich",
            crawled=False
        )
        blogger = Blogger(
            seed=seed,
            email_address='grimson32@gmail.com',
            domain="http://eatingmywaythroughoc.blogspot.com/"
        )
        analyzer = BloggerDomainAnalyzer(blogger.domain)
        crawler = BloggerDomainCrawler(blogger, analyzer, limit=2)
        blogger = crawler.start()
        self.assertTrue(blogger.scrubbed_tags)

    def test_return_sort_links_with_priority(self):
        links = ['this.com', 'this.com/about']
        self.assertTrue(sort_links_with_priority(links)[0] == 'this.com/about')