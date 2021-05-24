from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from sample_app.views import (BioView, BuffetView, ContactView, FingerView,
                              ImprintView, IndexView, InspireView, PrivacyView,
                              RequestView, ServiceView, TermsView, WorldView,
                              DrinksView, LunchView, EventsView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view()),
    url(r'kontakt$', ContactView.as_view()),
    url(r'busy-bee-world$', WorldView.as_view()),
    url(r'jetzt-anfragen$', RequestView.as_view()),
    url(r'datenschutz$', PrivacyView.as_view()),
    url(r'impressum', ImprintView.as_view()),
    url(r'agb', TermsView.as_view()),
    url(r'buffet-menue', BuffetView.as_view()),
    url(r'fingerfood', FingerView.as_view()),
    url(r'inspiration', InspireView.as_view()),
    url(r'bio-und-allergene-welt', BioView.as_view()),
    url(r'full-service', ServiceView.as_view()),
    url(r'getraenke', DrinksView.as_view()),
    url(r'office-lunch', LunchView.as_view()),
    url(r'event-consulting', EventsView.as_view()),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns
