from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from sample_app.views import IndexView, ContactView, WorldView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view()),
    url(r'kontakt$', ContactView.as_view()),
    url(r'busy-bee-world$', WorldView.as_view()),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns
