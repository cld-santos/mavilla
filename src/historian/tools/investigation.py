from .database import Database, Url


class Investigation():
    def __init__(self):
        self.db = Database()

    def register_unprocessed_urls(self, urls, parent=None):
        if not urls or not isinstance(urls, list):
            return

        existent_urls = [item.url for item in self.all_urls()]
        for url in urls:
            if url in existent_urls:
                continue

            self.db.save_url(Url(**{'url': url, 'parent': parent}))
            existent_urls.append(url)

    def save_url(self, url_address):
        return self.db.save_url(Url(**{'url': url_address}))

    def mark_as_processed(self, url):
        url.processed = True
        self.db.update_url(url)

    def unprocessed_urls(self):
        return self.db.get_unprocessed_urls()

    def processed_urls(self):
        return self.db.get_processed_urls()

    def all_urls(self):
        return self.db.get_all_urls()
