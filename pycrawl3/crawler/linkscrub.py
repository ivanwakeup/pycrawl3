from urllib.parse import urlparse

from utils.logger import crawler_log as log


def scrub(links, base_occurences=10):
    log.debug("LINKS: {}\n\n".format(links))

    urlp = []
    for link in links:
        try:
            lp = urlparse(link)
            urlp.append(lp)
        except:
            log.error("BLEW UP ON: {}".format(link))
            continue

    urls_base = [x.scheme + "://" + x.netloc for x in urlp]
    base_count = [urls_base.count(x) for x in urls_base]
    urls_full = [x.scheme + "://" + x.netloc + x.path for x in urlp]

    base_and_count = zip(urls_base, base_count)

    log.debug("BASECOUNT: {}\n\n".format(base_and_count))

    full_base_count = zip(urls_full, base_and_count)

    log.debug("FULLBASE: {}\n\n".format(full_base_count))

    new_linklist = []
    for item in full_base_count:
        if item[1][1] < base_occurences:
            new_linklist.append(item[0])

    return new_linklist
