class Trie():

    def __init__(self):
        self._end = '*'
        self.trie = dict()

    def __repr__(self):
        return repr(self.trie)

    def make_trie(self, *words):
        trie = dict()
        for word in words:
            temp_dict = trie
            for letter in word:
                temp_dict = temp_dict.setdefault(letter, {})
            temp_dict[self._end] = self._end
        return trie

    def has_word(self, word):
        sub_trie = self.trie

        for letter in word:
            if letter in sub_trie:
                sub_trie = sub_trie[letter]
            else:
                return False
        else:
            if self._end in sub_trie:
                return True
            else:
                return False

    def has_prefix(self, prefix):
        if not prefix:
            return False
        sub_trie = self.trie
        for letter in prefix:
            if letter in sub_trie:
                sub_trie = sub_trie[letter]
            else:
                return False
        return True

    def add_word(self, word):
        if self.has_word(word):
            print("Word Already Exists")
            return self.trie

        temp_trie = self.trie
        for letter in word:
            if letter in temp_trie:
                temp_trie = temp_trie[letter]
            else:
                temp_trie = temp_trie.setdefault(letter, {})
        temp_trie[self._end] = self._end
        return temp_trie
