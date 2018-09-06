import unittest
from pycrawl3.emails.blacklist import Blacklist
from pycrawl3.utils.Trie import Trie
from pycrawl3.emails.emails import EmailRanker
from settings.common import BASE_DIR


class TestCrawler(unittest.TestCase):

    def test_google_for_urls(self):
        pass

    def test_blacklist(self):
        blacklist = Blacklist(scrub_words=['info'])
        self.assertTrue(blacklist.is_blacklisted("info@dudeman.com"))
        blacklist = Blacklist(scrub_words=['guy'])
        self.assertTrue(blacklist.is_blacklisted("guy@dudeman.com"))
        blacklist = Blacklist(scrub_words=['something'])
        self.assertFalse(blacklist.is_blacklisted("notsome@dudeman.com"))

    def test_email_blacklist(self):
        blacklist = Blacklist.factory("emails")
        self.assertTrue(blacklist.is_blacklisted("info@dudeman.com"))
        self.assertFalse(blacklist.is_blacklisted("guy@dudeman.com"))


    def test_trie(self):
        trie = Trie()
        trie.add_word("david")
        trie.add_word("dallin")
        self.assertTrue(trie.has_prefix("dav"))
        self.assertFalse(trie.has_prefix("daa"))
        self.assertFalse(trie.has_prefix(""))
        self.assertFalse(trie.has_prefix("00"))

        self.assertTrue(trie.has_word("david"))
        self.assertFalse(trie.has_word("dallind"))
        self.assertFalse(trie.has_word(""))


    def test_email_ranker(self):
        base = BASE_DIR + '/../static/pycrawl3/'
        ranker = EmailRanker(base+'sales_words.txt', base+'person_names.txt', base+'top_sites.txt')
        print(ranker.rank_email('james.whitbrook@gizmodo.com'))



