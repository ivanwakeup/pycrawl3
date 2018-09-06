from pycrawl3.utils.Trie import Trie
from pycrawl3.utils.logger import log


class EmailRanker(object):
    scrub_words = None
    names_trie = None
    domain_scrub = None

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
        f.close()
        self.names_trie = trie

    def __build_domain_scrub(self, domain_file):
        scrub_words = set()
        f = open(domain_file, 'r')
        for line in f:
            scrub_words.add(line.lower().strip())
        f.close()
        self.domain_scrub = scrub_words

    def __email_contains_name(self, email):
        # traverse emails string to determine if a name is present
        i = 0
        j = 1
        while i < len(email) and j < len(email):
            # if the tree contains the prefix, keep searching the rest of the string
            if self.names_trie.has_prefix(email[i:j]):
                if self.names_trie.has_word(email[i:j]):
                    return True
                else:
                    j += 1
            else:
                i += 1
                j = i + 1
        return False

    def __email_contains_top_urls(self, email):
        parsed = email.split("@")
        if len(parsed) > 1:
            return parsed[1] in self.domain_scrub
        return False

    def rank_email(self, email):
        num_count = 0
        for letter in email:
            if letter.isnumeric():
                num_count += 1
                if num_count > 6:
                    return 3
        for word in self.scrub_words:
            if word in email:
                return 3
        providers = ['gmail', 'hotmail', 'aol', 'yahoo']
        for prov in providers:
            if prov in email:
                return 1

        if self.__email_contains_name(email):
            log.debug("email: {} contains name, checking against top urls...\n".format(email))
            if not self.__email_contains_top_urls(email):
                log.debug("email: {} not found in top urls...\n".format(email))
                return 2
        return 3
