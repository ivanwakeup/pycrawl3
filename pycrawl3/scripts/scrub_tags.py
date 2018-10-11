import django
if not hasattr(django, 'apps'):
    django.setup()

from django.conf import settings
from pycrawl3.settings import common

if not settings.configured:
    settings.configure(default_settings=common, DEBUG=True)

from pycrawl3.models import Blogger
from pycrawl3.crawler.analyzer import TagScrubber
import ast

bloggers = Blogger.objects.all()

for blogger in bloggers:
    tags = blogger.tags.split(",")
    scrubbed_tags = TagScrubber().scrub_tags(tags)
    blogger.scrubbed_tags = ",".join(scrubbed_tags)
    blogger.save()
    # try:
    #     new_tags = ast.literal_eval(blogger.tags)
    #     new_tags = ",".join(new_tags).strip()
    #     blogger.tags = new_tags
    #     blogger.save()
    # except:
    #     print("tags are ok already")
    #     continue