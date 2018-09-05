from pycrawl3.utils.Trie import Trie


class EmailRanker(object):

    scrub_words = None
    names_trie = None

    def __init__(self, scrub_words_file=None, names_file=None):
        self.__build_scrub_list(scrub_words_file)
        self.__build_names_trie(names_file)


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




