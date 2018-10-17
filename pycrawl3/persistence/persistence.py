from os.path import expanduser
from pycrawl3.models import Email, Seed, Blogger
from django.db import transaction
from django.db.models import F
from pycrawl3.utils.logger import log
from django.db.utils import OperationalError


class EmailDelegate(object):

    def __init__(self, writer, email_blacklist, ranker=None):
        self.__writer = writer
        self.blacklist = email_blacklist
        self.ranker = ranker

    def add_email(self, email, url, seed=None):
        if not self.blacklist.is_blacklisted(email):
            try:
                exists = Email.objects.get(email_address=email)
                log.info("Email {} found, updating....".format(email))
                exists.modified_count = F('modified_count') + 1
                exists.save()
                return
            except Email.DoesNotExist:
                pass
            email_model = Email(seed_url=seed, email_address=email.lower(), from_url=url, tier=self.get_email_tier(email))
            self.__writer.add_data(email_model)

    def get_email_tier(self, email):
        return self.ranker.rank_email(email)


class SeedDelegate(object):

    __writer = None

    def __init__(self, writer, blacklist=None):
        self.__writer = writer
        self.blacklist = blacklist

    def add_seed(self, url):
        seed_model = Seed(url=url, crawled=False)
        self.__writer.add_data(seed_model)

    @staticmethod
    def get_seeds_to_crawl():
        seeds = Seed.objects.filter(crawled=False)
        return list(seeds)

    @staticmethod
    def set_crawled(seed):
        seed.crawled = True
        seed.save()

    @staticmethod
    def add_or_update_seed(seed):
        existing_seeds = Seed.objects.filter(url=seed.url)
        if existing_seeds:
            log.info("Seed or Seeds {} found, updating....".format(seed.url))
            for e_seed in existing_seeds:
                e_seed.modified_count = F('modified_count') + 1
                e_seed.crawled = seed.crawled
                e_seed.weighted_terms = seed.weighted_terms
                e_seed.search_term = seed.search_term
                e_seed.save()
            return
        else:
            log.info("new Seed {} being saved to DB".format(seed))
            seed.save()

    @staticmethod
    def add_seed_or_pass(seed):
        try:
            exists = Seed.objects.get(url=seed.url)
            log.debug("seed found, doing nothing...")
            return
        except Seed.MultipleObjectsReturned:
            log.debug("multiple seeds found, doing nothing...")
        except Seed.DoesNotExist:
            seed.save()

class BloggerDelegate(object):

    __writer = None

    def __init__(self, writer, blacklist=None):
        self.__writer = writer
        self.blacklist = blacklist

    #unfortunately, you can run into race conditions here. I'm not sure what the fix is short of implementing some
    #queueing mechanism for db writes.
    def add_blogger(self, blogger):
        try:
            e_blogger = Blogger.objects.get(email_address=blogger.email_address)
            log.info("blogger {} already found. proceeding...".format(blogger))
            e_blogger.modified_count = F('modified_count') + 1
            e_blogger.save()
        except Blogger.MultipleObjectsReturned:
            log.info("blogger {} already found. proceeding...".format(blogger))
        except Blogger.DoesNotExist:
            log.info("new blogger {} being saved to DB".format(blogger))
            blogger.save()

class Writer(object):

    def __init__(self, batch_size):
        self.data = set()
        self.batch_size = batch_size

    def add_data(self, model_data):
        log.info("adding %s to persistence" % model_data)
        self.data.add(model_data)
        self.check_should_write()

    def empty_data(self):
        self.data = set()

    def check_should_write(self):
        if len(self.data) >= self.batch_size:
            self.write()

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


class PostgresWriter(Writer):

    def __init__(self, batch_size):
        super(PostgresWriter, self).__init__(batch_size)

    @transaction.atomic
    def write(self):
        log.info("WRITING BATCH TO DB!!!!")
        for model in self.data:
            try:
                model.save()
            except Exception as e:
                log.info("FAILED TO WRITE RECORD: {} WITH EXCEPTION: {}".format(model, e))
        self.empty_data()