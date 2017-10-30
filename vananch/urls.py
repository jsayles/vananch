from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.map, name='home'),
    url(r'^map/(?P<import_id>\d+)$', views.map, name='map'),
    url(r'^import/$', views.ship_import, name='import'),
    url(r'^admin/', admin.site.urls),
]
