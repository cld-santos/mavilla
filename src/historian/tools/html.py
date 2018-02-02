#!/usr/bin/env python3
import time
from selenium import webdriver
from html.parser import HTMLParser


class HtmlParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.document = {}
        self.actual_tag = []

    def handle_starttag(self, tag, attrs):
        self.actual_tag.append('id_{0}'.format(str(time.time())))
        actual_tag_idx = len(self.actual_tag) - 1
        parent = self.actual_tag[actual_tag_idx - 1] if (actual_tag_idx - 1) >= 0 else None

        self.document[self.actual_tag[actual_tag_idx]] = {
            'tag': tag,
            'parent': parent,
            'attributes': {key: value for key, value in attrs},
            'data': None
        }

    def handle_endtag(self, tag):
        self.actual_tag.pop()

    def handle_data(self, data):
        if (len(self.actual_tag) > 0): 
            self.document[self.actual_tag[len(self.actual_tag) - 1]]['data'] = data


class HtmlFinder():

    def __init__(self, document):
        self.document = document

    def find_by(self, subject):
        subject = subject.lower()
        elements_found = []
        for idx in self.document:
            element = self.document[idx]
            data = element.get('data', "")
            if data and element.get('tag') != 'a' and subject in data.lower():
                elements_found.append(self.document[idx])
        return elements_found

    def find_references_by(self, subject):
        subject = subject.lower()
        elements_found = []
        for idx in self.document:
            element = self.document[idx]
            data = element.get('data', "")
            if data and element.get('tag') == 'a' and subject in data.lower():
                elements_found.append(self.document[idx])
        return elements_found

    def find_references(self):
        elements_found = []
        for idx in self.document:
            element = self.document[idx]
            data = element.get('data', "")
            if data and element.get('tag') == 'a':
                elements_found.append(self.document[idx])
        return elements_found


def get_html_from(url):
    driver = webdriver.PhantomJS()
    driver.set_window_size(1024, 600)
    driver.get(url)
    html_page = driver.page_source
    driver.quit()

    parser = HtmlParser()
    parser.feed(html_page)

    return parser.document
