from pycrawl3.crawler.url_ops import *
from pycrawl3.settings.common import BASE_DIR
from pycrawl3.tagging.tagger import Tagger, Stemmer, Reader, Rater
from pycrawl3.emails.emails import EmailRanker
import pickle


class BloggerDomainAnalyzer(object):
    domain_doc = ""
    domain = None
    tags = None

    base = BASE_DIR + '/../static/pycrawl3/'
    ranker = EmailRanker(base + 'sales_words.txt', base + 'common_names_sorted.txt', base + 'top_sites.txt')

    def __init__(self):
        self.responses = list()
        self.emails = set()

    def addEmails(self, emails):
        self.emails.update(emails)

    def addDomain(self, domain):
        if not self.domain:
            self.domain = domain

    def addResponse(self, response):
        self.responses.append(response)

    def flush(self):
        for email in self.emails:
            if self.ranker.rank_email(email) == 1:
                self.__build_doc()
                self.__build_tags()
                self.__clean_tags()
                print((self.domain, self.emails, self.tags))
                break
        self.cleanup()

    def __build_doc(self):
        for response in self.responses:
            self.domain_doc += get_visible_text(response.text)

    def __build_tags(self):
        print('Loading dictionary... ')
        dic = BASE_DIR + "/tagging/data/dict.pkl"
        weights = pickle.load(open(dic, 'rb'))

        tagger = Tagger(Reader(), Stemmer(), Rater(weights))

        self.tags = tagger(self.domain_doc)

    def __clean_tags(self):
        def has_digits(s):
            for char in s:
                if char.isdigit():
                    return True
            return False
        new_tags = []
        for tag in self.tags:
            new_tag = str(tag.string)
            if not has_digits(new_tag) and len(new_tag) >= 3:
                new_tags.append(new_tag)
        self.tags = new_tags

    def cleanup(self):
        self.responses.clear()
        self.emails.clear()
        self.tags = None
        self.domain = None
        self.domain_doc = ""

    def is_blog(self):
        blog_words = ["blog", "blogger"]
        if self.domain_doc != "":
            for word in blog_words:
                if word in self.domain_doc:
                    return True
        for email in self.emails:
            if self.ranker.rank_email(email) < 3:
                return True
        return False