from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'pages/index.html'


class ContactView(TemplateView):
    template_name = 'pages/kontakt.html'


class WorldView(TemplateView):
    template_name = 'pages/world.html'


class RequestView(TemplateView):
    template_name = 'pages/anfrage.html'


class PrivacyView(TemplateView):
    template_name = 'pages/datenschutz.html'


class ImprintView(TemplateView):
    template_name = 'pages/impressum.html'


class TermsView(TemplateView):
    template_name = 'pages/agb.html'
