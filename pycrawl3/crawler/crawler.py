import logging
import re
from collections import deque
from urllib.parse import urlparse

import requests
import requests.exceptions
from bs4 import BeautifulSoup

from .blacklist import Blacklist
from .linkscrub import scrub
from .timeout import TimeoutError
from ..writer.writer import EmailDelegate, PostgresWriter


def get_url_extras(url):
    parts = urlparse(url)
    try:
        base_url = "{0.scheme}://{0.netloc}".format(parts)
    except UnicodeEncodeError:
        base_url = None
    path = url[:url.rfind('/') + 1] if '/' in parts.path else url
    return url, base_url, path


def get_url_response(url):
    print("Processing %s" % url)
    try:
        response = requests.get(url, timeout=3)
    except requests.exceptions.RequestException as e:
        print("{} failed: {}".format(url, str(e)))
        response = None
    return response


def get_email_set_from_response(url_response):
    emails = set(re.findall(
        r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", url_response.text, re.I))
    return emails


def crawl_from_url(url_string):
    queue = deque()
    queue.append(url_string)
    eo = crawl(queue)
    print(eo)


def crawl(links):
    blacklist = Blacklist.factory("url", list(links))
    links_to_process = deque(blacklist.remove_blacklisted())
    email_blacklist = Blacklist.factory("email")
    writer = PostgresWriter()
    delegate = EmailDelegate(writer, email_blacklist)
    processed_urls = set()
    emails = set()

    logger = logging.getLogger()

    while links_to_process:
        url1 = links_to_process.pop()
        # add to processed immediately, to support failure
        processed_urls.add(url1)

        url_extras = get_url_extras(url1)

        response = get_url_response(url1)
        if not response or not response.ok:
            continue

        try:
            new_emails = get_email_set_from_response(response)
        except TimeoutError:
            continue

        for email in new_emails:
            delegate.add_email(email, url1)

        # create a beautiful soup for the html document

        soup = BeautifulSoup(response.text, "html.parser")

        # find and process all the anchors in the document
        for anchor in soup.find_all("a"):
            # extract link url from the anchor
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            # resolve relative links
            if link.startswith('/'):
                link = url_extras[1] + link
            elif not link.startswith('http'):
                link = url_extras[2] + link

            # add the new url to the queue if it was not enqueued nor processed yet
            if link not in links_to_process and link not in processed_urls:
                if not blacklist.is_blacklisted(link):
                    links_to_process.appendleft(link)

        # scrub linkset to ensure crawler doesn't waste time on one site
        # urls = scrub_linkset(urls)
        urls_list = list(links_to_process)
        scrubbed = scrub(urls_list, 4)
        logger.debug(scrubbed)
        links_to_process = deque(scrubbed)

    return emails
