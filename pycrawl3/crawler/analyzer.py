from pycrawl3.crawler.url_ops import *
from pycrawl3.settings.common import BASE_DIR
from pycrawl3.tagging.tagger import Tagger, Stemmer, Reader, Rater
from pycrawl3.emails.emails import EmailRanker
import pickle
from pycrawl3.utils.logger import log


class BloggerDomainAnalyzer(object):
    domain_doc = ""
    domain = None
    tags = None
    filter_words = set()
    best_email = None

    base = BASE_DIR + '/static/pycrawl3/'
    ranker = EmailRanker(base + 'sales_words.txt', base + 'common_names_sorted.txt', base + 'top_sites.txt')

    def __init__(self, blog_delegate=None, file=BASE_DIR+"/tagging/data/filter_words.txt"):
        self.responses = list()
        self.emails = set()
        self.delegate = blog_delegate
        try:
            self.__init_filter_words(file)
        except FileNotFoundError:
            log.info("no filter_word file found, proceeding without one...")

    def addEmails(self, emails):
        self.emails.update(emails)

    def addDomain(self, domain):
        if not self.domain:
            self.domain = domain

    def addResponse(self, response):
        self.responses.append(response)

    def __init_filter_words(self, file):
        f = open(file, 'r')
        for line in f:
            self.filter_words.add(line.lower().strip())
        f.close()

    def analyze(self):
        for email in self.emails:
            if self.ranker.rank_email(email) == 1:
                self.best_email = email
                self.__build_doc()
                self.__build_tags()
                self.__clean_tags()
                print(self.domain, self.emails, self.tags)
        return self.domain, self.best_email, self.tags

    def flush(self):
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
        def has_special(s):
            for char in s:
                if char in ["/"]:
                    return True
            return False
        new_tags = []
        for tag in self.tags:
            new_tag = str(tag.string)
            if new_tag not in self.filter_words \
                    and not has_digits(new_tag) \
                    and not has_special(new_tag) and len(new_tag) >= 3:
                new_tags.append(new_tag)
        self.tags = new_tags[:10]

    def cleanup(self):
        self.responses.clear()
        self.emails.clear()
        self.tags = None
        self.domain = None
        self.domain_doc = ""
        self.best_email = None

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