import coreapi
from rest_framework.filters import BaseFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
from hydroserver.renderers import WaterMLRenderer, WaterJSONRenderer
from hydroserver_wof import wof_database_models, wof_response_models
from hydroserver_wof.utilities import get_response_info, get_wof_response
from hydroserver_wof import serializers
from drf_yasg.utils import swagger_auto_schema


class Sites(viewsets.ViewSet):

    renderer_classes = (WaterMLRenderer, WaterJSONRenderer,)

    def get_sites(self, request, network_id, database_id, *args, **kwargs):
        """
        GET Sites

        Gets a list of available sites from a database.
        
        REST URL Pattern: ~/wof/{network_id}/{database_id}/sites/?(format= # )

        :param network: The network ID where the database is located.
        :param database: The database ID to get sites from.
        """

        databases = {
            "odm2_sqlite": wof_database_models.odm2_sqlite.get_sites
        }

        outputs = {
            "waterml": wof_response_models.waterml_1_1.get_sites,
            "waterjson": wof_response_models.waterjson_1_1.get_sites
        }

        content_type = request.META.get("HTTP_ACCEPT")

        response_format, response_type = get_response_info(content_type)

        params = {
            "network": network_id,
            "database": database_id,
            "format": response_format,
            "query_url": request.build_absolute_uri()
        }

        response = get_wof_response(databases, outputs, params)

        if response == "404_Not_Found":
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif response == "400_Bad_Request":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status.HTTP_200_OK, content_type=response_type)


class SiteInfo(viewsets.ViewSet):

    renderer_classes = (WaterMLRenderer, WaterJSONRenderer,)

    @swagger_auto_schema(query_serializer=serializers.SiteInfoSerializer)
    def get_site_info(self, request, network_id, database_id, *args, **kwargs):
        """
        GET Site Info

        Gets information for a single site from a database.
        
        Rest URL Pattern: ~/wof/{network_id}/{database_id}/siteInfo/?(site_code= # &format= # )

        :param network: The network ID where the database is located.
        :param database: The database ID to get the site info from.
        :param variable_code: The site code of the site of interest.
        """

        databases = {
            "odm2_sqlite": wof_database_models.odm2_sqlite.get_site_info
        }

        outputs = {
            "waterml": wof_response_models.waterml_1_1.get_site_info,
            "waterjson": wof_response_models.waterjson_1_1.get_site_info
        }

        content_type = request.META.get("HTTP_ACCEPT")

        response_format, response_type = get_response_info(content_type)

        params = {
            "network": network_id,
            "database": database_id,
            "format": response_format,
            "query_url": request.build_absolute_uri(),
            "site_code": request.GET.get("site_code")
        }

        response = get_wof_response(databases, outputs, params)

        if response == "404_Not_Found":
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif response == "400_Bad_Request":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status.HTTP_200_OK, content_type=response_type)


class Variables(viewsets.ViewSet):

    renderer_classes = (WaterMLRenderer, WaterJSONRenderer,)

    def get_variables(self, request, network_id, database_id, *args, **kwargs):
        """
        GET Variables

        Gets a list of available variables from a database.
        
        REST URL Pattern: ~/wof/{network_id}/{database_id}/variables/?(format= # )

        :param network: The network ID where the database is located.
        :param database: The database ID to get variables from.
        """

        databases = {
            "odm2_sqlite": wof_database_models.odm2_sqlite.get_variables
        }

        outputs = {
            "waterml": wof_response_models.waterml_1_1.get_variables,
            "waterjson": wof_response_models.waterjson_1_1.get_variables
        }

        content_type = request.META.get("HTTP_ACCEPT")

        response_format, response_type = get_response_info(content_type)

        params = {
            "network": network_id,
            "database": database_id,
            "format": response_format,
            "query_url": request.build_absolute_uri()
        }

        response = get_wof_response(databases, outputs, params)

        if response == "404_Not_Found":
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif response == "400_Bad_Request":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status.HTTP_200_OK, content_type=response_type)


class VariableInfo(viewsets.ViewSet):

    renderer_classes = (WaterMLRenderer, WaterJSONRenderer,)

    @swagger_auto_schema(query_serializer=serializers.VariableInfoSerializer)
    def get_variable_info(self, request, network_id, database_id, *args, **kwargs):
        """
        GET Variable Info

        Gets information for a single variable from a database.
        
        Rest URL Pattern: ~/wof/{network_id}/{database_id}/variableInfo/?(variable_code= # &format= # )

        :param network: The network ID where the database is located.
        :param database: The database ID to get the variable info from.
        :param variable_code: The variable code of the variable of interest.
        """

        databases = {
            "odm2_sqlite": wof_database_models.odm2_sqlite.get_variable_info
        }

        outputs = {
            "waterml": wof_response_models.waterml_1_1.get_variable_info,
            "waterjson": wof_response_models.waterjson_1_1.get_variable_info
        }

        content_type = request.META.get("HTTP_ACCEPT")

        response_format, response_type = get_response_info(content_type)

        params = {
            "network": network_id,
            "database": database_id,
            "format": response_format,
            "query_url": request.build_absolute_uri(),
            "variable_code": request.GET.get("variable_code")
        }

        response = get_wof_response(databases, outputs, params)

        if response == "404_Not_Found":
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif response == "400_Bad_Request":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status.HTTP_200_OK, content_type=response_type)


class Values(viewsets.ViewSet):

    renderer_classes = (WaterMLRenderer, WaterJSONRenderer,)

    @swagger_auto_schema(query_serializer=serializers.ValuesSerializer)
    def get_values(self, request, network_id, database_id, *args, **kwargs):
        """
        GET Values

        Gets time series values given a variable, site, start time, and end time.
        
        Rest URL Pattern: ~/wof/{network_id}/{database_id}/values/?(site_code= # &variable_code= # &start_time= # &end_time= # &format= # )

        :param network: The network ID where the database is located.
        :param database: The database ID to get time series values from.
        :param site_code: The site code used to obtain the time series values.
        :param variable_code: The variable code used to obtain the time series values.
        :param start_time: The start time of the time series.
        :param end_time: The end time of the time series.
        """

        databases = {
            "odm2_sqlite": wof_database_models.odm2_sqlite.get_values
        }

        outputs = {
            "waterml": wof_response_models.waterml_1_1.get_values,
            "waterjson": wof_response_models.waterjson_1_1.get_values
        }

        content_type = request.META.get("HTTP_ACCEPT")

        response_format, response_type = get_response_info(content_type)

        params = {
            "network": network_id,
            "database": database_id,
            "format": response_format,
            "query_url": request.build_absolute_uri(),
            "site_code": request.GET.get("site_code"),
            "variable_code": request.GET.get("variable_code"),
            "start_time": request.GET.get("start_date"),
            "end_time": request.GET.get("end_date")
        }

        response = get_wof_response(databases, outputs, params)

        if response == "404_Not_Found":
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif response == "400_Bad_Request":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status.HTTP_200_OK, content_type=response_type)
