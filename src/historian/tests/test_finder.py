#!/usr/bin/env python3
from unittest import TestCase
from historian.tools.scraper import HtmlParser, HtmlFinder


class TestFinder(TestCase):

    def test_must_found_a_subject_mentioned(self):
        fifi_parser = HtmlParser()
        fifi_parser.feed('<html>    <body>      <div class="item">meu item 1            <div>           <a href="link-1">teste</a>          </div>      </div>      <div class="item">meu item 2            <div>               <a href="link-2">teste</a>          </div>      </div>      <div class="item">meu item 3            <div>               <a href="link-3">alvo</a>           </div>      alvo</div>  </body></html>')
        finder = HtmlFinder(fifi_parser.document)
        result = finder.find_by('alvo')
        self.assertEqual(1, len(result))

    def test_must_found_a_uppercase_subject(self):
        fifi_parser = HtmlParser()
        fifi_parser.feed('<html>    <body>      <div class="item">            <div>           <a href="link-1">teste</a>          </div>      </div>      <div class="item">meu item 2            <div>               <a href="link-2">teste</a>          </div>      </div>      <div class="item">meu item 3            <div>               <a href="link-3">alvo</a>           </div>     alvo </div>  meu item 1</body></html>')
        finder = HtmlFinder(fifi_parser.document)
        result = finder.find_by('ALVO')
        self.assertEqual(1, len(result))

    def test_must_not_found_a_subject(self):
        fifi_parser = HtmlParser()
        fifi_parser.feed('<html>    <body>      <div class="item">meu item 1            <div>           <a href="link-1">teste</a>          </div>      </div>      <div class="item">meu item 2            <div>               <a href="link-2">teste</a>          </div>      </div>      <div class="item">meu item 3            <div>               <a href="link-3">alvo</a>           </div>      </div>  </body></html>')
        finder = HtmlFinder(fifi_parser.document)
        result = finder.find_by('termo inexistente')
        self.assertEqual(0, len(result))

    def test_must_found_a_complex_subject(self):
        fifi_parser = HtmlParser()
        fifi_parser.feed('<html>    <body>      <div class="item">meu item 1            <div>           <a href="link-1">teste</a>          </div>      </div>      <div class="item">meu item 2            <div>               <a href="link-2">teste</a>          </div>      </div>      <div class="item">meu item 3            <div>               <a href="link-3">Alvo Existente</a>           </div>Alvo Existente      </div>  </body></html>')
        finder = HtmlFinder(fifi_parser.document)
        result = finder.find_by('Alvo Existente')
        self.assertEqual(1, len(result))

    def test_must_found_more_than_one_subject(self):
        fifi_parser = HtmlParser()
        fifi_parser.feed('<html>    <body>      <div class="item">meu item 1            <div>           <a href="link-1">teste</a>          </div>      </div>      <div class="item">meu item 2            <div>               <a href="link-2">LInk</a>          </div>Alvo Existente      </div>      <div class="item">meu item 3            <div>               <a href="link-3">Link</a>           </div>Alvo Existente      </div>  </body></html>')
        finder = HtmlFinder(fifi_parser.document)
        result = finder.find_by('Alvo Existente')
        self.assertEqual(2, len(result))

    def test_must_found_references_to_subject(self):
        fifi_parser = HtmlParser()
        fifi_parser.feed('<html>    <body>      <div class="item">meu item 1            <div>           <a href="link-1">teste</a>          </div>      </div>      <div class="item">meu item 2            <div>               <a href="link-2">LInk</a>          </div>Alvo Existente      </div>      <div class="item">meu item 3            <div>               <a href="link-3">Link</a>           </div>Alvo Existente      </div>  </body></html>')
        finder = HtmlFinder(fifi_parser.document)
        result = finder.find_references_by('link')
        self.assertEqual(2, len(result))
