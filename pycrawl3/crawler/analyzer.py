from pycrawl3.crawler.url_ops import *
from pycrawl3.settings.common import BASE_DIR
from pycrawl3.tagging.tagger import Tagger, Stemmer, Reader, Rater
from pycrawl3.emails.emails import EmailRanker
import pickle
from pycrawl3.utils.logger import log
from pycrawl3.crawler.blacklist import FileBlacklist
import re

DICTIONARY_BASE = BASE_DIR + '/dictionaries/'


class DomainAnalyzer(object):

    def __init__(self, domain, email_ranker=None):
        self.domain_doc = ""
        self.domain = domain
        self.tags = None
        self.responses = list()
        self.emails = set()
        self.best_email = None
        self.emailranker = email_ranker
        if not self.emailranker:
            self.emailranker = EmailRanker(DICTIONARY_BASE + 'sales_words.txt', DICTIONARY_BASE + 'common_names_sorted.txt',
                                 DICTIONARY_BASE + 'top_sites.txt')

    def add_emails(self, emails):
        self.emails.update(emails)

    def add_response(self, response):
        self.responses.append(response)

    def analyze(self):
        for email in self.emails:
            if self.emailranker.rank_email(email) == 1:
                self.best_email = email
                self.__build_doc()
                self.__build_tags()
                log.info((self.domain, self.emails, self.tags))
        return self.domain, self.best_email, self.emails, self.tags

    def __build_doc(self):
        for response in self.responses:
            self.domain_doc += get_visible_text(response.text)

    def __build_tags(self):
        print('Loading dictionary... ')
        dic = BASE_DIR + "/tagging/data/dict.pkl"
        with open(dic, 'rb') as f:
            weights = pickle.load(f)

        tagger = Tagger(Reader(), Stemmer(), Rater(weights))

        tags = tagger(self.domain_doc)
        self.tags = [str(tag.string) for tag in tags]

    def cleanup(self, new_domain):
        self.responses.clear()
        self.emails.clear()
        self.domain = new_domain
        self.tags = None
        self.domain_doc = ""
        self.best_email = None


class BloggerDomainData:

    def __init__(self, **kwargs):
        allowed_keys = [
            'ranked_emails',
            'domain',
            'found_impressions',
            'found_ads',
            'tags',
            'category',
            'found_phone'
        ]
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)


class BloggerDomainAnalyzer(object):

    def __init__(self, domain, email_ranker=None, tag_scrubber=None):
        self.responses = list()
        self.emails = set()
        self.domain_doc = ""
        self.domain = domain
        self.tags = None
        self.found_impressions = None
        self.found_ads = None
        self.category = None
        self.emailranker = email_ranker
        self.tagscrubber = tag_scrubber
        if not self.emailranker:
            self.emailranker = EmailRanker(DICTIONARY_BASE + 'sales_words.txt', DICTIONARY_BASE + 'common_names_sorted.txt', DICTIONARY_BASE + 'top_sites.txt')
        if not self.tagscrubber:
            self.tagscrubber = TagScrubber()

    def analyze(self):
        ranked_emails = self.rank_emails()
        self.__build_doc()
        self.__build_tags()
        scrubbed_tags = self.tagscrubber.scrub_tags(self.tags)
        self.__analyze_words()
        data = BloggerDomainData(ranked_emails=ranked_emails, domain=self.domain, tags=scrubbed_tags, category=self.category)
        return data

    def __build_doc(self):
        for response in self.responses:
            self.domain_doc += get_visible_text(response.text)

    def __build_tags(self):
        print('Loading dictionary... ')
        dic = BASE_DIR + "/tagging/data/dict.pkl"
        with open(dic, 'rb') as f:
            weights = pickle.load(f)

        tagger = Tagger(Reader(), Stemmer(), Rater(weights))

        tags = tagger(self.domain_doc)
        self.tags = [str(tag.string) for tag in tags]

    def cleanup(self, new_domain):
        self.responses.clear()
        self.emails.clear()
        self.domain = new_domain
        self.tags = None
        self.domain_doc = ""
        self.found_impressions = None
        self.found_ads = None
        self.category = None

    def add_emails(self, emails):
        self.emails.update(emails)

    def add_response(self, response):
        self.responses.append(response)

    def rank_emails(self):
        ranked = []
        for email in self.emails:
            ranked.append((email, self.emailranker.rank_email(email)))
        return sorted(ranked, key=lambda x: x[1])





    def __analyze_words(self):
        word_list = get_word_list(self.domain_doc)
        counts = Counter(word_list)
        ad_words = ["advertising", "advertise"]
        for word in ad_words:
            if word in counts:
                self.found_ads = True
        if "impressions" in counts:
            self.found_impressions = True


class TagScrubber(object):

    def __init__(self, filter_phrases=DICTIONARY_BASE+'tag_filter_phrases.txt', contains_words=DICTIONARY_BASE+'tag_filter_words.txt'):
        print(contains_words)
        self.filter_words = FileBlacklist.get_blacklist_set(contains_words)
        self.filter_phrases = FileBlacklist.get_blacklist_set(filter_phrases)

    def scrub_tags(self, taglist):
        if self.is_foreign_language(taglist):
            return []
        result = self.filterdigits(taglist)
        result = self.filtershorttags(result)
        result = self.remove_special(result)
        result = self.filterwords(self.filter_words, result)
        result = self.filterphrases(self.filter_phrases, result)
        result = self.dedupe_and_strip(result)
        return result

    @staticmethod
    def is_foreign_language(taglist):
        foreign_count = 0
        for tag in taglist:
            try:
                tag.encode(encoding='utf-8').decode('ascii')
            except UnicodeDecodeError:
                foreign_count += 1
        try:
            pct = foreign_count/len(taglist)
            if pct > .6:
                return True
        except ZeroDivisionError:
            return False
        return False

    @staticmethod
    def remove_special(taglist):
        special_regex = r"(^\/|^&|&$|^-|-$|#|^'|'$)"
        for i in range(len(taglist)):
            taglist[i] = re.sub(special_regex, '', taglist[i]).strip()

        return taglist

    @staticmethod
    def filterwords(contains_words, taglist):
        for i in range(len(taglist)):
            for word in contains_words:
                if word in taglist[i]:
                    taglist[i] = taglist[i].replace(word, '').strip()
        return taglist

    @staticmethod
    def filterdigits(taglist):
        return list(filter(lambda x: not any(char.isdigit() for char in x), taglist))


    @staticmethod
    def filtershorttags(taglist):
        return list(filter(lambda x: not len(x) < 3, taglist))

    @staticmethod
    def filterphrases(filter_phrases, taglist):
        return list(filter(lambda x: not x in filter_phrases, taglist))

    @staticmethod
    def dedupe_and_strip(taglist):
        taglist = [tag.strip() for tag in taglist]
        taglist = list(filter(lambda x: not x == '', taglist))
        taglist = list(set(taglist))
        return taglist