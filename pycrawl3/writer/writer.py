from os.path import expanduser
from ..models import Email
from django.db import transaction
from ..utils.logger import log


class EmailDelegate(object):

    __writer = None

    def __init__(self, writer, blacklist=None):
        self.__writer = writer
        self.blacklist = blacklist

    def add_email(self, email, url, seed=None):
        if not self.blacklist.is_blacklisted(email):
            email_model = Email(seed_url=seed, email_address=email, from_url=url, tier=self.get_email_tier(email))
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

    def __init__(self):
        self.data = set()
        self.__should_write = False

    def add_data(self, model_data):
        log.info("adding %s to writer" % model_data)
        self.check_should_write()
        self.data.add(model_data)

    def empty_data(self):
        self.data = set()

    def check_should_write(self):
        if self.__should_write:
            self.write()
        elif len(self.data) > 1:
            self.__should_write = True

    def write(self):
        return


class TextFileWriter(Writer):

    __homedir = expanduser("~")
    __filename = None

    def __init__(self, filename="emails.txt"):
        self.__filename = filename
        super(TextFileWriter, self).__init__()

    def write(self):
        f = open(self.__filename, 'a')
        for email_model in self.data:
            f.write("%s\n" % "{}|{}".format(email_model.email_address, email_model.tier))
        f.close()
        self.empty_data()
        self.__should_write = False


class PostgresWriter(Writer):

    def __init__(self):
        super(PostgresWriter, self).__init__()

    @transaction.atomic
    def write(self):
        log.info("WRITING BATCH TO DB!!!!")
        for email_model in self.data:
            email_model.save()
        self.empty_data()
        self.__should_write = False