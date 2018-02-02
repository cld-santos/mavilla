from django.http import HttpResponse
from django.template import loader, Context
from django.views import View
from historian.investigation import Investigation


class Index(View):
    def get(self, request):
        # template = loader.get_template('base.html')
        # rendered_template = template.render(Context())

        investigation = Investigation('http://claudio-santos.com/')
        investigation.investigate_unprocessed_url(investigation.unprocessed_urls())

        return HttpResponse('')
