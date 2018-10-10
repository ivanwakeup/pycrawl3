class Blacklist(object):
    def __init__(self, scrub_words=None, scrub_list=None):
        if scrub_list is not None:
            self.scrub_list = scrub_list
        self.scrub_words = scrub_words

    def is_blacklisted(self, url):
        blacklisted = False
        for x in self.scrub_words:
            if x in url:
                blacklisted = True

        return blacklisted

    def remove_blacklisted(self):
        return [x for x in self.scrub_list if not self.is_blacklisted(x)]

    def factory(type, scrub_list=None, file=None):
        if type == "url":
            return UrlBlacklist(scrub_list)
        if type == "ext":
            return ExtensionBlacklist(scrub_list)
        if type == "emails":
            return EmailBlacklist(scrub_list)
        if type == "file":
            return FileBlacklist(file)

    factory = staticmethod(factory)


class UrlBlacklist(Blacklist):
    blacklist = ['twitter',
                 'facebook',
                 'wikipedia',
                 'wikidata',
                 'plus.google.com',
                 'pinterest.com',
                 'yelp.com',
                 'google.com',
                 'youtube.com',
                 'amazon.com',
                 'tripadvisor.com',
                 'olark.com',
                 'instagram',
                 'aboutads.info']

    def __init__(self, scrub_list):
        super(UrlBlacklist, self).__init__(self.blacklist, scrub_list)


class EmailBlacklist(Blacklist):
    blacklist = ['example', 'emails', 'support', 'domain', 'orders', 'info', 'github', 'registration', 'mozilla',
                     'donate', 'feedback', 'newsletter', 'name', 'noreply', 'team', 'admin', 'security', 'about', 'media', 'contact', 'customer',
                 'enablejs']

    def __init__(self, scrub_list=None):
        super(EmailBlacklist, self).__init__(self.blacklist, scrub_list)


class ExtensionBlacklist(Blacklist):
    blacklist = ['.jpg', '.png', '.jpeg', '.mp3', '.tgz']

    def __init__(self, scrub_list):
        super(ExtensionBlacklist, self).__init__(self.blacklist, scrub_list)


class FileBlacklist(object):
    blacklist = set()

    def __init__(self, file):
        self.__init_read_blacklist(file)

    def __init_read_blacklist(self, file):
        f = open(file, 'r')
        for line in f:
            self.blacklist.add(line.lower().strip())
        f.close()

    def is_blacklisted(self, item):
        if item in self.blacklist:
            return True
        return False

    @staticmethod
    def get_blacklist_set(file):
        result = set()
        with open(file, 'r') as f:
            for line in f:
                result.add(line.lower().strip())
        return result