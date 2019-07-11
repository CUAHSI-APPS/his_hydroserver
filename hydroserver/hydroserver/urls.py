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
      title="Water Data Server API",
      default_version='v1.0',
      description="Water Data Server Rest API",
      contact=openapi.Contact(email="kjlippold@gmail.com")
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   url=settings.PROXY_BASE_URL
)

urlpatterns = [
    url(r'^wds/admin/', admin.site.urls),
    url(r'^wds/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^wds/manage/', include('hydroserver_core.urls')),
    url(r'^wds/wof/', include('hydroserver_wof.urls')),
    url(r'^wds/refts/', include('hydroserver_refts.urls')),
]
