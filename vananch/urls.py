from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView

from . import views

admin.autodiscover()

favicon_view = RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^favicon\.ico$', favicon_view),

    url(r'^$', views.map, name='home'),
    url(r'^map/(?P<import_id>\d+)$', views.map, name='map'),
    url(r'^import/$', views.ship_import, name='import'),

    url(r'^admin/', admin.site.urls),
]
