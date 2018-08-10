from os.path import expanduser
from ..models import Email
from django.db import transaction

class EmailDelegate(object):

    __writer = None

    def __init__(self, writer, blacklist=None):
        self.__writer = writer
        self.blacklist = blacklist

    def add_email(self, email, url):
        if not self.blacklist.is_blacklisted(email):
            email_model = Email(email_address=email, from_url=url, tier=self.get_email_tier(email))
            self.__writer.add_data(email_model)

    def add_emails(self, emails):
        for email, url in emails:
            if not self.blacklist.is_blacklisted(email):
                email_model = Email(email_address=email, from_url=url, tier=self.get_email_tier(email))
                self.__writer.add_data(email_model)

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

    def add_data(self, model_data):
        self.__check_should_write()
        self.__data.add(model_data)

    def __empty_data(self):
        self.__data = set()

    def __check_should_write(self):
        if self.__should_write:
            self.write()
        elif len(self.__data) > 10:
            self.__should_write = True

    def write(self):
        return


class TextFileWriter(Writer):

    __homedir = expanduser("~")
    __filename = None

    def __init__(self, filename="emails.txt"):
        self.__filename = filename
        super()

    def write(self):
        f = open(self.__filename, 'a')
        for email_model in self.__data:
            f.write("%s\n" % "{}|{}".format(email_model.email_address, email_model.tier))
        f.close()
        self.__empty_data()
        self.__should_write = False


class PostgresWriter(Writer):

    def __init__(self):
        super()

    @transaction.atomic
    def write(self):
        for email_model in self.__data:
            email_model.save()
        self.__empty_data()
        self.__should_write = False