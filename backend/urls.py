from django.conf.urls import url
from backend import views
from django.contrib import admin


urlpatterns = [
    url(r'^api/get_last_n_items/(?P<n>.+)/$', views.get_last_n_items),
    url(r'^admin/', admin.site.urls),
]