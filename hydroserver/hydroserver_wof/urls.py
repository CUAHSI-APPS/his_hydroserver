from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from hydroserver_wof import views


urlpatterns = [
    url(r'^GetSites/$', views.GetSites.as_view({'get': 'get_sites'})),
    url(r'^GetSiteInfo/$', views.GetSiteInfo.as_view({'get': 'get_site_info'})),
    url(r'^GetVariables/$', views.GetVariables.as_view({'get': 'get_variables'})),
    url(r'^GetVariableInfo/$', views.GetVariableInfo.as_view({'get': 'get_variable_info'})),
    url(r'^GetValues/$', views.GetValues.as_view({'get': 'get_values'})),
]

urlpatterns = format_suffix_patterns(urlpatterns)
