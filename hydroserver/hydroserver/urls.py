from django.contrib import admin
from django.urls import include
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from hydroserver import settings


schema_view = get_schema_view(
   openapi.Info(
      title="HydroServer API",
      default_version='v1.0',
      description="HydroServer Rest API",
      contact=openapi.Contact(email="kjlippold@gmail.com")
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   url=settings.PROXY_BASE_URL
)

urlpatterns = [
    url(r'^hydroserver/admin/', admin.site.urls),
    url(r'^hydroserver/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^hydroserver/rest/', include('hydroserver_core.rest_api.urls')),
    url(r'^hydroserver/wof/', include('hydroserver_wof.urls')),
]
