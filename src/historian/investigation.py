from .tasks.investigate import investigate
from .tools.database import Database, Url


class Investigation():
    def __init__(self, url_address):
        self.db = Database()
        self.db.save_url(Url(**{'url': url_address}))

    def _register_unprocessed_urls(self, urls, parent=None):
        if not urls or not isinstance(urls, list):
            return

        existent_urls = [item.url for item in self.all_urls()]
        for url in urls:
            if url in existent_urls:
                continue

            self.db.save_url(Url(**{'url': url, 'parent': parent}))
            existent_urls.append(url)

    def investigate_unprocessed_url(self, urls):
        if not urls or len(urls) == 0:
            return

        for url in urls:
            print('investigating:', url.url)
            urls_unprocessed = investigate(url.url)
            url.processed = True
            self.db.update_url(url)
            if not urls_unprocessed:
                continue

            self._register_unprocessed_urls(urls_unprocessed, parent=url._id)

        un_urls = self.unprocessed_urls()
        if un_urls:
            self.investigate_unprocessed_url(un_urls)

    def unprocessed_urls(self):
        return self.db.get_unprocessed_urls()

    def processed_urls(self):
        return self.db.get_processed_urls()

    def all_urls(self):
        return self.db.get_all_urls()