#!/usr/bin/env python3
from unittest import TestCase
from historian.tools.scraper import HtmlParser


class TestHtmlParser(TestCase):

    def test_must_read_a_simple_html(self):
        parser = HtmlParser()
        parser.feed('<html><body><div class="item">meu item 1</div><div class="item">meu item 2</div><div class="item">meu item 3</div></body></html>')
        self.assertEqual(5, len(parser.document))

    def test_must_read_html(self):
        a_count = 0
        parser = HtmlParser()
        parser.feed('<html>    <body>      <div class="item">meu item 1            <div>           <a href="link-1">teste</a>          </div>      </div>      <div class="item">meu item 2            <div>               <a href="link-2">teste</a>          </div>      </div>      <div class="item">meu item 3            <div>               <a href="link-3">teste</a>          </div>      </div>  </body></html>')

        for idx in parser.document:
            element = parser.document[idx]
            if element.get('tag', None) == 'a':
                a_count += 1
                parent = element.get('parent', None)
                if parent:
                    self.assertEqual(parser.document[parent]['tag'], 'div')

        self.assertEqual(a_count, 3)

    def test_must_read_a_element_with_attributes(self):
        parser = HtmlParser()
        parser.feed('<html><body><div class="item">meu <a target="_blank" href="link-1">item</a> item 1</div></body></html>')
        self.assertEqual(4, len(parser.document))
        for idx in parser.document:
            element = parser.document[idx]
            if element.get('tag', None) == 'a':
                attributes = element.get('attributes', [])
                self.assertEqual(len(attributes), 2)
                self.assertEqual(attributes['href'], 'link-1')

