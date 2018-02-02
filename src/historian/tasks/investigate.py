from __future__ import absolute_import, unicode_literals
import re
from celery import group
from website.celery import app
from ..tools.html import HtmlFinder, get_html_from

http_pattern = r'^http[s]?://'
url_pattern = r'(http[s]?://[a-zA-Z0-9.\-\_]+/?)'


def to_one_dimension(matrix):
    one_dimension = []
    for item in matrix:
        if isinstance(item, list):
            one_dimension.extend(to_one_dimension(item))
        else:
            one_dimension.append(item)
    return one_dimension


@app.task(bind=True)
def look_for_references(self, url):
    urls = []
    
    document = get_html_from(url)
    finder = HtmlFinder(document)

    # Finding references (aka links)
    references = finder.find_references()
    for reference in references:
        attributes = reference.get('attributes')
        href = attributes.get('href', None)
        if not href or href == url:
            continue

        if not re.match(http_pattern, href.lower()):
            url_match = re.findall(url_pattern, url)
            url_base = url_match[0] if len(url_match) > 0 else ""
            href = '{0}/{1}'.format(url_base, href)
            href = href.split('?')[0] + "/" if '?' in href else href

        urls.append(href)

    return urls if len(urls) > 0 else None


def investigate(urls):
    if not urls:
        return []

    if isinstance(urls, list):
        group_execution = group([look_for_references.s(_url) for _url in urls])
        promise = group_execution()
    else:
        promise = look_for_references.delay(urls)

    promise.wait()

    return promise.get()
