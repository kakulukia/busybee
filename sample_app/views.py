from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "pages/index.html"


class ContactView(TemplateView):
    template_name = "pages/kontakt.html"


class WorldView(TemplateView):
    template_name = "pages/world.html"


class RequestView(TemplateView):
    template_name = "pages/anfrage.html"


class PrivacyView(TemplateView):
    template_name = "pages/datenschutz.html"


class ImprintView(TemplateView):
    template_name = "pages/impressum.html"


class TermsView(TemplateView):
    template_name = "pages/agb.html"


class BuffetView(TemplateView):
    template_name = "pages/buffet.html"


class FingerView(TemplateView):
    template_name = "pages/finger.html"


class InspireView(TemplateView):
    template_name = "pages/inspiration.html"


class BioView(TemplateView):
    template_name = "pages/bio.html"


class ServiceView(TemplateView):
    template_name = "pages/service.html"


class DrinksView(TemplateView):
    template_name = "pages/drinks.html"


class LunchView(TemplateView):
    template_name = "pages/lunch.html"


class EventsView(TemplateView):
    template_name = "pages/events.html"
