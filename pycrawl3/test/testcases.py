import unittest
from blacklist import Blacklist
from pycrawl3.utils.Trie import Trie


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
        pass
        # base = BASE_DIR + '/../static/pycrawl3/'
        # ranker = EmailRanker(base+'sales_words.txt', base+'common_names_sorted.txt', base+'top_sites.txt')
        # tier2 = '/Users/ivanwakeup/tier2.csv'
        #
        # f = open(tier2, 'r')
        # emails = []
        # for line in f:
        #     emails.append(line.lower().strip())
        # f.close()
        #
        # f = open('/Users/ivanwakeup/emailst2.csv', 'a')
        # for email in emails:
        #     (email, rank) = (email, ranker.rank_email(email))
        #     if rank == 2:
        #         print(email, rank)
        #         f.write(email+"\n")
        # f.close()




