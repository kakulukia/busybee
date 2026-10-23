from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from bee.views import (
    BioView,
    BuffetView,
    ContactView,
    FingerView,
    ImprintView,
    IndexView,
    InspireView,
    PrivacyView,
    RequestView,
    ServiceView,
    TermsView,
    WorldView,
    DrinksView,
    LunchView,
    EventsView,
    ContactDoneView,
    RequestDoneView,
)

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^$", IndexView.as_view()),
    re_path(r"kontakt$", csrf_exempt(ContactView.as_view())),
    re_path(r"kontakt-danke$", ContactDoneView.as_view()),
    re_path(r"busy-bee-world$", WorldView.as_view()),
    re_path(r"jetzt-anfragen$", csrf_exempt(RequestView.as_view())),
    re_path(r"jetzt-anfragen-danke$", RequestDoneView.as_view()),
    re_path(r"datenschutz$", PrivacyView.as_view()),
    re_path(r"impressum", ImprintView.as_view()),
    re_path(r"agb", TermsView.as_view()),
    re_path(r"buffet-menue", BuffetView.as_view()),
    re_path(r"fingerfood", FingerView.as_view()),
    re_path(r"inspiration", InspireView.as_view()),
    re_path(r"bio-und-allergene-welt", BioView.as_view()),
    re_path(r"full-service", ServiceView.as_view()),
    re_path(r"getraenke", DrinksView.as_view()),
    re_path(r"office-lunch", LunchView.as_view()),
    re_path(r"event-consulting", EventsView.as_view()),
    path("captcha/", include("captcha.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [re_path(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns
