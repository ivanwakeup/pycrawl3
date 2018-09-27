from django.db import models


class Email(models.Model):
    email_address = models.CharField("Email Address", primary_key=True, max_length=255, null=False)
    seed_url = models.CharField("Seed Url", max_length=255, null=True)
    from_url = models.CharField("Url Extracted From", max_length=255, null=True)
    tier = models.IntegerField()
    createdTime = models.DateTimeField("Created Time", auto_now_add=True)
    modifiedTime = models.DateTimeField("Modified Time", auto_now=True, null=True)


class Seed(models.Model):
    url = models.CharField("Url", primary_key=True, max_length=255, null=False)
    crawled = models.BooleanField("Url Crawled")
    crawl_count = models.IntegerField("Crawl Count", default=0)
    createdTime = models.DateTimeField("Created Time", auto_now_add=True)
    modifiedTime = models.DateTimeField("Updated Time", auto_now=True, null=True)