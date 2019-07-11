from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from hydroserver_core import views

urlpatterns = [
    url(r"^networks/$", views.Networks.as_view({"get": "get_networks", "post": "post_network"}), name="networks"),
    url(r"^databases/$", views.DatabaseList.as_view({"get": "get_database_list"})),
    url(r"^network/(?P<network_id>[\w\-]+)/$", views.Network.as_view({"get":"get_network", "delete":"delete_network"}), name="network"),
    url(r"^network/(?P<network_id>[\w\-]+)/databases/$", views.Databases.as_view({"get":"get_databases", "post":"post_database"}), name="databases"),
    url(r"^network/(?P<network_id>[\w\-]+)/database/(?P<database_id>.*)/$", views.Database.as_view({"get":"get_database", "delete":"delete_database"}), name="database"),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=None)
