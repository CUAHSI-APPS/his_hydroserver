from rest_framework.filters import BaseFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
import coreschema
import coreapi
from drf_yasg import openapi
from hydroserver.renderers import ReftsRenderer, GeoJSONRenderer
from hydroserver_core.models import Reference as ReferenceModel
from drf_yasg.utils import swagger_auto_schema
from hydroserver_refts import serializers
from hydroserver_refts import refts_response_models
from hydroserver_refts.utilities import get_response_info, get_refts_response


class ReftsCatalog(viewsets.ViewSet):

    renderer_classes = (ReftsRenderer, GeoJSONRenderer,)

    @swagger_auto_schema(query_serializer=serializers.ReftsCatalogSerializer)
    def get_catalog(self, request, *args, **kwargs):
        """
        GET Refts Catalog

        Gets reference timeseries catalog for the server.

        REST URL Pattern: ~/refts/catalog/

        """

        outputs = {
            "reftsjson": refts_response_models.refts_json.get_refts,
            "reftsgeojson": refts_response_models.refts_geojson.get_refts
        }

        content_type = request.META.get("HTTP_ACCEPT")

        response_format, response_type = get_response_info(content_type)

        params = {
            "site_name": request.GET.getlist("site_name"),
            "site_code": request.GET.getlist("site_code"),
            "variable_name": request.GET.getlist("variable_name"),
            "variable_code": request.GET.getlist("variable_code"),
            "sample_medium": request.GET.getlist("sample_medium"),
            "method_link": request.GET.getlist("method_link"),
            "return_type": request.GET.get("return_type"),
            "service_type": request.GET.get("service_type"),
            "ref_type": request.GET.get("ref_type"),
            "min_value_count": request.GET.get("min_value_count"),
            "max_value_count": request.GET.get("max_value_count"),
            "begin_date": request.GET.get("start_date"),
            "end_date": request.GET.get("end_date"),
            "north": request.GET.get("north"),
            "south": request.GET.get("south"),
            "east": request.GET.get("east"),
            "west": request.GET.get("west"),
            "network_id": request.GET.getlist("network_id"),
            "database_id": request.GET.getlist("database_id")
        }

        response = get_refts_response(outputs, params, response_format)

        if response == "404_Not_Found":
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        elif response == "400_Bad_Request":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status.HTTP_200_OK)


class ReftsParameters(viewsets.ViewSet):

    @swagger_auto_schema(query_serializer=serializers.ReftsParameterSerializer)
    def get_parameters(self, request, *args, **kwargs):
        """
        GET Refts Parameters

        Gets list of parameter values for the reference timeseries catalog.

        REST URL Pattern: ~/refts/parameters/
        """

        parameter_list = request.GET.getlist("parameter")
        parameter_response = {}

        if "site_name" in parameter_list or len(parameter_list) == 0:
            site_names = ReferenceModel.objects.order_by().values_list("site_name", flat=True).distinct()
            if site_names:
                parameter_response["site_names"] = list(filter(None, site_names))
        if "site_code" in parameter_list or len(parameter_list) == 0:
            site_codes = ReferenceModel.objects.order_by().values_list("site_code", flat=True).distinct()
            if site_codes:
                parameter_response["site_codes"] = list(filter(None, site_codes))
        if "variable_name" in parameter_list or len(parameter_list) == 0:
            variable_names = ReferenceModel.objects.order_by().values_list("variable_name", flat=True).distinct()
            if variable_names:
                parameter_response["variable_names"] = list(filter(None, variable_names))
        if "variable_code" in parameter_list or len(parameter_list) == 0:
            variable_codes = ReferenceModel.objects.order_by().values_list("variable_code", flat=True).distinct()
            if variable_codes:
                parameter_response["variable_codes"] = list(filter(None, variable_codes))
        if "sample_medium" in parameter_list or len(parameter_list) == 0:
            sample_mediums = ReferenceModel.objects.order_by().values_list("sample_medium", flat=True).distinct()
            if sample_mediums:
                parameter_response["sample_mediums"] = list(filter(None, sample_mediums))
        if "method_link" in parameter_list or len(parameter_list) == 0:
            method_links = ReferenceModel.objects.order_by().values_list("method_link", flat=True).distinct()
            if method_links:
                parameter_response["method_links"] = list(filter(None, method_links))

        if not parameter_response:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(parameter_response)
