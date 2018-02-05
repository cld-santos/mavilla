from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('historian', include=['historian.tasks.investigate'])
app.config_from_object('historian.conf')


if __name__=="__main__":
    app.start()

