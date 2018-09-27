import unittest
from pycrawl3.crawler.analytics import *


class TestAnalytics(unittest.TestCase):

    url = 'http://www.runningdiva.ph/tag/mountain-trail/'
    response = get_url_response(url)
    visible_text = get_visible_text(response.text)
    print(visible_text)
    word_list = get_word_list(visible_text)

    def test_get_words_from_html(self):
        count_text = filter_stop_words(self.word_list)
        counts = get_word_count(count_text)
        counts.sort(key=lambda x: x[1])
        print(counts)

    def test_filter_stop_words(self):
        pass
