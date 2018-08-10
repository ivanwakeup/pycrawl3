from os.path import expanduser
from ..models import Email


class EmailDelegate(object):

    __writer = None

    def __init__(self, writer, blacklist=None):
        self.__writer = writer
        self.blacklist = blacklist

    def add_email(self, email, url):
        if not self.blacklist.is_blacklisted(email):
            obj = Email(email_address=email, from_url=url, tier=self.get_email_tier(email))
            self.__writer.add_data(obj)

    def add_emails(self, emails):
        obj_set = set()
        for email, url in emails:
            if not self.blacklist.is_blacklisted(email):
                obj = Email(email_address=email, from_url=url, tier=self.get_email_tier(email))
            obj_set.add(obj)
        self.__Email_set.update(obj_set)

    def get_email_tier(self, email):
        tier1 = ["gmail", "yahoo", "hotmail", "aol"]
        for tier in tier1:
            if tier in email:
                return 1
        return 2


class Writer(object):

    __data = set()
    __should_write = False

    def __init__(self):
        super()


class TextFileWriter(Writer):

    __homedir = expanduser("~")

    def __init__(self):
        super()

    def add_data(self, model_data):
        self.__check_should_write()
        self.__data.add(model_data)

    def __check_should_write(self):
        if self.__should_write:
            self.write()
        elif len(self.__data) > 10:
            self.__should_write = True

    def __empty_data(self):
        self.__data = set()

    def write(self, filename):
        f = open(filename, 'a')
        for email in self.__data:
            f.write("%s\n" % email)
        f.close()
        self.__empty_data()
        self.__should_write = False


class PostgresWriter(Writer):

    def __init__(self):
        super()

    def add_data(self, data):
        self.__check_should_write()
        self.__data.add(data)

    def __check_should_write(self):
        if self.__should_write:
            self.write()
        elif len(self.__data) > 10:
            self.__should_write = True

    def __empty_data(self):
        self.__data = set()

    def write(self):
        self.__empty_data()
        self.__should_write = False