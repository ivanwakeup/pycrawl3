from django.db import models


class Email(models.Model):
    email_address = models.CharField("Email Address", max_length=1000, primary_key=True, null=False)
    seed_url = models.CharField("Seed Url", max_length=1000, null=True)
    from_url = models.CharField("Url Extracted From", max_length=1000, null=True)
    tier = models.IntegerField()
    modified_count = models.IntegerField(default=0)
    created_time = models.DateTimeField("Created Time", auto_now_add=True)
    modified_time = models.DateTimeField("Modified Time", auto_now=True, null=True)

    def save(self, *args, **kwargs):
        self.modified_count += 1
        return super(Email, self).save(*args, **kwargs)


class Seed(models.Model):
    url = models.CharField("Url", primary_key=True, max_length=1000, null=False)
    crawled = models.BooleanField("Url Crawled")
    crawl_count = models.IntegerField("Crawl Count", default=0)
    created_time = models.DateTimeField("Created Time", auto_now_add=True)
    modified_time = models.DateTimeField("Updated Time", auto_now=True, null=True)


class Blogger(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    tags = models.CharField("Tags", max_length=1000, null=True)
    created_time = models.DateTimeField("Created Time", auto_now_add=True)
    modified_time = models.DateTimeField("Modified Time", auto_now=True)