import django
if not hasattr(django, 'apps'):
    django.setup()

from django.conf import settings
from pycrawl3.settings import common

if not settings.configured:
    settings.configure(default_settings=common, DEBUG=True)

from pycrawl3.models import Blogger
from pycrawl3.crawler.scoring import score_blogger

bloggers = Blogger.objects.all()

for blogger in bloggers:
    blogger.sc
