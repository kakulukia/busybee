from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'pages/index.html'


class ContactView(TemplateView):
    template_name = 'pages/kontakt.html'


class WorldView(TemplateView):
    template_name = 'pages/world.html'
