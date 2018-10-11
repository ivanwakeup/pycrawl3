from django.db import models


class Email(models.Model):
    email_address = models.CharField("Email Address", max_length=1000, primary_key=True, null=False)
    seed_url = models.CharField("Seed Url", max_length=1000, null=True)
    from_url = models.CharField("Url Extracted From", max_length=1000, null=True)
    tier = models.IntegerField()
    modified_count = models.IntegerField(default=0)
    created_time = models.DateTimeField("Created Time", auto_now_add=True)
    modified_time = models.DateTimeField("Modified Time", auto_now=True)


class Seed(models.Model):
    url = models.CharField("Url", primary_key=True, max_length=1000, null=False)
    search_term = models.CharField("Search Term", max_length=255, null=True, blank=True)
    crawled = models.BooleanField("Url Crawled")
    crawl_count = models.IntegerField("Crawl Count", default=0)
    created_time = models.DateTimeField("Created Time", auto_now_add=True, null=True)
    modified_time = models.DateTimeField("Updated Time", auto_now=True, null=True)


class Blogger(models.Model):
    email_address = models.CharField("Email Address", max_length=1000, primary_key=True, null=False)
    other_emails = models.CharField("Other Emails", max_length=2000, null=True, blank=True)
    search_term = models.CharField("Search Term", max_length=1000, null=True, blank=True)
    domain = models.CharField("Domain", max_length=1000, null=True)
    tags = models.CharField("Tags", max_length=1000, null=True)
    scrubbed_tags = models.CharField("Scrubbed Tags", max_length=1000, null=True, blank=True)
    modified_count = models.IntegerField(default=0)
    created_time = models.DateTimeField("Created Time", auto_now_add=True)
    modified_time = models.DateTimeField("Modified Time", auto_now=True)

    def __str__(self):
        uid = str(self.email_address) + '  --  ' + str(self.domain) + '  --  ' + str(self.search_term)
        return uid