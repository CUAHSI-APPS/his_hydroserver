from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from hydroserver_core.refts import views


urlpatterns = [
    url(r'^network/(?P<network_id>[\w\-]+)/refts/$', views.NetworkRefts.as_view({"get":"get_network_refts"}), name="network_refts"),
    url(r'^network/(?P<network_id>[\w\-]+)/database/(?P<database_id>.*)/refts/$', views.DatabaseRefts.as_view({"get":"get_database_refts"}), name="database_refts"),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=None)
