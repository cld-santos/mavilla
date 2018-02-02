import os

DEBUG = False
ALLOWED_HOSTS = ["claudio-santos.com", "simplologia.com.br", "localhost", ]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'production'

ROOT_URLCONF = "website.urls"

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'historian',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
        ]
    },
]

WSGI_APPLICATION = 'website.wsgi.application'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

CELERY_IMPORTS = ('historian.tasks',)
CELERY_BROKER_URL = 'amqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'amqp://guest@localhost//'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_ANNOTATIONS = {
    'tasks.add': {'rate_limit': '5/m'}
}

CELERY_TASK_ALWAYS_EAGER = False