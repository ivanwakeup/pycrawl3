from django.db import models


class Email(models.Model):
    email_address = models.CharField("Email Address", primary_key=True, max_length=255, null=False)
    seed_url = models.CharField("Seed Url", max_length=255, null=True)
    from_url = models.CharField("Url Extracted From", max_length=255, null=True)
    tier = models.IntegerField()
    createdAt = models.DateTimeField("Created Time", auto_now=True)


class Seed(models.Model):
    url = models.CharField("Url", max_length=255, null=False)
    crawled = models.BooleanField("Url Crawled")
    updatedAt = models.DateTimeField("Updated Time", auto_now=True)