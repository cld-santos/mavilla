from __future__ import absolute_import, unicode_literals
import re
from celery import chain
from socketIO_client import SocketIO
from ..celery import app
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
def look_for_references(self, url, collection=None):
    if not url and not url['url']:
        return

    urls = []

    if not isinstance(url, Url):
        url = Url(**url)

    investigation = Investigation(collection=collection)
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

    investigation.update_url(url, processed=True)

    return urls


@app.task(bind=True)
def investigate_it(self, urls, parent=None, collection=None):
    socketIO = SocketIO('localhost', 5000)
    investigation = Investigation(collection=collection)

    for url in urls:
        try:
            _url = investigation.save_url(url, parent=parent)
            socketIO.emit('sendMessage', {'data': _url.to_dict()})
            chain_of_execution = chain(
                look_for_references.s(_url.to_dict(), collection=collection),
                investigate_it.s(parent=_url._id, collection=collection)
            )
            chain_result = chain_of_execution()
            _url.child_task_id = chain_result.id
            investigation.update_url(_url, child_task_id=chain_result.id)
            return chain_result.id
        except Exception as e:
            print(e)
            print('This URL "{0}" has already been registred.'.format(urls))


