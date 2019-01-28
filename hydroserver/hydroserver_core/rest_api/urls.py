from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from hydroserver_core.rest_api import views


urlpatterns = [
    url(r'^networks/$', views.Networks.as_view({"get":"get_networks", "post":"post_network"}), name="networks"),
    url(r'^network/(?P<network_id>[\w\-]+)/$', views.NetworkDetails.as_view({"get":"get_network_details", "delete":"delete_network"}), name="network_details"),
    url(r'^network/(?P<network_id>[\w\-]+)/databases/$', views.Databases.as_view({"get":"get_databases", "post":"post_database"}), name="databases"),
    url(r'^network/(?P<network_id>[\w\-]+)/database/(?P<database_id>[\w\-]+)/$', views.DatabaseDetails.as_view({"get":"get_database_details", "delete":"delete_database"}), name='database_details'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=None)
