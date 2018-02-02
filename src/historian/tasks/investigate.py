from __future__ import absolute_import, unicode_literals
import re
from celery import group
from website.celery import app
from ..tools.html import HtmlFinder, get_html_from
from ..tools.investigation import Investigation
from ..tools.database import Url
from bson.objectid import ObjectId


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
    investigation = Investigation()
    if not isinstance(url, Url):
        url = Url(**url)

    urls = []
    document = get_html_from(url.url)
    finder = HtmlFinder(document)

    # Finding references (aka links)
    references = finder.find_references()
    for reference in references:
        attributes = reference.get('attributes')
        href = attributes.get('href', None)
        if not href or href == url.url:
            continue

        if not re.match(http_pattern, href.lower()):
            url_match = re.findall(url_pattern, url.url)
            url_base = url_match[0] if len(url_match) > 0 else ""
            href = '{0}/{1}'.format(url_base, href)
            href = href.split('?')[0] + "/" if '?' in href else href

        urls.append(href)

    investigation.mark_as_processed(url)
    investigation.register_unprocessed_urls(urls, url.url)


@app.task(bind=True)
def investigate(self, urls, investigation=None):
    db = Investigation()

    if isinstance(urls, list):
        _list_aux = [look_for_references.s(_url) for _url in urls]
        _list_aux.append(investigate.s(db.unprocessed_urls()))
        group_execution = group(_list_aux)
        group_execution()
        
    else:
        saved_url = db.save_url(urls)
        _url = saved_url.__dict__
        _url['_id'] = str(_url['_id'])
        group_execution = group(look_for_references.s(_url), investigate.s(db.unprocessed_urls()))
        group_execution()

    
