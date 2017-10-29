from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.map, name='map'),
    url(r'^admin/', admin.site.urls),
]
