from .database import Database, Url


class Investigation():
    def __init__(self, database=None):
        self.db = database if database else Database()

    def register_unprocessed_urls(self, urls, parent=None):
        res = []
        if not urls or not isinstance(urls, list):
            return

        existent_urls = [item.url for item in self.all_urls()]
        for url in urls:
            if url in existent_urls:
                continue

            try:
                _url = self.save_url(url, parent=parent)
                res.append(_url.to_dict())
                existent_urls.append(url)
            except:
                pass
        return res

    def save_url(self, url_address, parent=None):
        return self.db.save_url(Url(**{'url': url_address, 'parent': parent}))

    def mark_as_processed(self, url):
        url.processed = True
        self.db.update_url(url)

    def unprocessed_urls(self):
        return self.db.get_unprocessed_urls()

    def processed_urls(self):
        return self.db.get_processed_urls()

    def all_urls(self):
        return self.db.get_all_urls()
