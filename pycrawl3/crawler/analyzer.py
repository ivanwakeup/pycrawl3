from pycrawl3.crawler.url_ops import *


class BloggerDomainAnalyzer(object):
    domain_doc = ""

    def __init__(self):
        self.responses = list()
        self.emails = set()

    def addEmails(self, emails):
        self.emails.update(emails)

    def addResponse(self, response):
        self.responses.append(response)

    def flush(self):
        self.__build_doc()
        print(self.domain_doc)
        self.responses.clear()
        self.emails.clear()
        self.domain_doc = ""

    def __build_doc(self):
        for response in self.responses:
            self.domain_doc += get_visible_text(response.text)