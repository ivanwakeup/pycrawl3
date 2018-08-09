from os.path import expanduser


class EmailDelegate(object):

    __emails = set()
    __writer = None

    def __init__(self, writer, blacklist=None):
        self.__writer = writer
        self.blacklist = blacklist

    def add_email(self, email):
        self.__writer.check_should_write()
        if not self.blacklist.is_blacklisted(email):
            self.__emails.add(email)

    def add_emails(self, emails):
        self.__check_should_write()
        if emails:
            for email in emails:
                if self.blacklist:
                    if not self.blacklist.is_blacklisted(email):
                        self.__emails.add(email)
                else:
                    self.__emails.add(email)

    def __check_should_write(self):
        if self.__should_write:
            self.write()
        elif len(self.__emails) > 10:
            self.__should_write = True

    def __sort_emails_into_tiers(self):
        for email in self.__emails:
            if EmailDelegate.is_tier_1(email):
                self.__tier_1_emails[1].add(email)
            else:
                self.__tier_2_emails[1].add(email)

    @staticmethod
    def is_tier_1(email):
        tier1 = ["gmail", "yahoo", "hotmail", "aol"]
        for tier in tier1:
            if tier in email:
                return True

    def __write_tier_1(self):
        filename, emails = self.__tier_1_emails
        f = open(filename, 'a')
        for email in emails:
            f.write("%s\n" % email)
        f.close()

    def __write_tier_2(self):
        filename, emails = self.__tier_2_emails
        f = open(filename, 'a')
        for email in emails:
            f.write("%s\n" % email)
        f.close()

    def __empty_email_sets(self):
        self.__tier_1_emails = ('{}/tier_1_emails.txt'.format(self.__homedir), set())
        self.__tier_2_emails = ('{}/tier_2_emails.txt'.format(self.__homedir), set())
        self.__emails = set()

    def write(self):
        self.__sort_emails_into_tiers()
        self.__write_tier_1()
        self.__write_tier_2()
        self.__empty_email_sets()
        self.__should_write = False


class Writer(object):

    __data = set()
    __should_write = False

    def __init__(self):
        super()


class TextFileWriter(Writer):

    __homedir = expanduser("~")

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