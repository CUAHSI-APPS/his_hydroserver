from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from hydroserver_refts import views


urlpatterns = [
    url(r'^catalog/', views.ReftsCatalog.as_view({'get': 'get_catalog'})),
    url(r'^parameters/', views.ReftsParameters.as_view({'get': 'get_parameters'})),
]

urlpatterns = format_suffix_patterns(urlpatterns)
