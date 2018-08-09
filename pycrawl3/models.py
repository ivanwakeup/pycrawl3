from django.db import models


class Email(models.Model):
    email_address = models.CharField("Email Address", max_length=255, null=False)
    from_url = models.CharField("Url Extracted From", max_length=255, null=True)
    createdAt = models.DateTimeField("Created Time", auto_now_add=True)
    updated_at = models.DateTimeField("Updated Time", auto_now=True)