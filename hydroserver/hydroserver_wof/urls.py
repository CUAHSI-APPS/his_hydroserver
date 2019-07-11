from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from hydroserver_wof import views


urlpatterns = [
    url(r'^(?P<network_id>[\w\-]+)/(?P<database_id>.*)/sites/$', views.Sites.as_view({'get': 'get_sites'})),
    url(r'^(?P<network_id>[\w\-]+)/(?P<database_id>.*)/site-info/$', views.SiteInfo.as_view({'get': 'get_site_info'})),
    url(r'^(?P<network_id>[\w\-]+)/(?P<database_id>.*)/variables/$', views.Variables.as_view({'get': 'get_variables'})),
    url(r'^(?P<network_id>[\w\-]+)/(?P<database_id>.*)/variable-info/$', views.VariableInfo.as_view({'get': 'get_variable_info'})),
    url(r'^(?P<network_id>[\w\-]+)/(?P<database_id>.*)/values/$', views.Values.as_view({'get': 'get_values'})),
]

urlpatterns = format_suffix_patterns(urlpatterns)
