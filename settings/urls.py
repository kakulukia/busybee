from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from bee.views import (BioView, BuffetView, ContactView, FingerView,
                       ImprintView, IndexView, InspireView, PrivacyView,
                       RequestView, ServiceView, TermsView, WorldView,
                       DrinksView, LunchView, EventsView, ContactDoneView, RequestDoneView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view()),
    url(r'kontakt$', csrf_exempt(ContactView.as_view())),
    url(r'kontakt-danke$', ContactDoneView.as_view()),
    url(r'busy-bee-world$', WorldView.as_view()),
    url(r'jetzt-anfragen$', csrf_exempt(RequestView.as_view())),
    url(r'jetzt-anfragen-danke$', RequestDoneView.as_view()),
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
    path('captcha/', include('captcha.urls')),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns
