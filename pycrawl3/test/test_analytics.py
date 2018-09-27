import unittest
from pycrawl3.crawler.analytics import *


class TestAnalytics(unittest.TestCase):

    def test_get_words_from_html(self):
        url = 'http://briansrunningadventures.com'
        response = get_url_response(url)
        visible_text = get_visible_text(response.text)
        counts = get_words_from_text(visible_text)
        counts.sort(key=lambda x: x[1])
        print(counts)