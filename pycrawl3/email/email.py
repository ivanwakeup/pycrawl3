from pycrawl3.utils.Trie import Trie


class EmailRanker(object):

    scrub_words = None
    names_trie = None

    def __init__(self, scrub_words_file=None, names_file=None, domain_file=None):
        if scrub_words_file:
            self.__build_scrub_list(scrub_words_file)
        if names_file:
            self.__build_names_trie(names_file)
        if domain_file:
            self.__build_domain_scrub(domain_file)

    def __build_scrub_list(self, words_file):
        scrub_words = []
        f = open(words_file, 'r')
        for line in f:
            scrub_words.append(line.strip())
        f.close()
        self.scrub_words = scrub_words

    def __build_names_trie(self, names_file):
        f = open(names_file, 'r')
        trie = Trie()
        for line in f:
            word = line.lower().strip()
            trie.add_word(word)
        self.names_trie = trie

    def __build_domain_scrub(self, domain_file):
        scrub_words = set()
        f = open(domain_file, 'r')
        for line in f:
            scrub_words.add(line.lower().strip())
        f.close()
        self.domain_scrub = scrub_words

    def rank_email(self, email):
        for word in self.scrub_words:
            if word in email:
                return 3
        providers = ['gmail', 'hotmail', 'aol', 'yahoo']
        for prov in providers:
            if prov in email:
                return 1

        #determine tier 2?
        name_trie = Trie()
        for name in self.names:
            name_trie.add




