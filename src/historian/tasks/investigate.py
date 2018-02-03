from __future__ import absolute_import, unicode_literals
import re
from celery import group, chain
from website.celery import app
from ..tools.scraper import HtmlFinder, get_html_from
from ..tools.investigation import Investigation
from ..tools.database import Url


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

    if not isinstance(url, Url):
        url = Url(**url)

    investigation = Investigation()
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
    return investigation.register_unprocessed_urls(urls, url.url)


@app.task(bind=True)
def investigate(self, urls, investigation=None):
    db = Investigation()

    if isinstance(urls, list):
        _list_aux = [chain(look_for_references.s(_url), investigate.s()) for _url in urls if _url and _url['url']]
        group_of_execution = group(_list_aux)
        group_of_execution()
    else:
        try:
            _url = db.save_url(urls)
            group_execution = chain(look_for_references.s(_url.to_dict()), investigate.s())
            group_execution()
        except Exception as e:
            print(e)
            print('This URL "{0}" has already been registred.'.format(urls))

    
