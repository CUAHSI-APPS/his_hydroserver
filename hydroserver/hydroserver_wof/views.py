from rest_framework.filters import BaseFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse
from hydroserver.renderers import HydroServerRenderer
from hydroserver_wof import wof_database_models, wof_output_models
import coreapi
from hydroserver_wof.utilities import get_content_type, get_wof_response, build_refts


class SitesFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='format',
            location='query',
            required=False,
            type='string'
        )]


class SiteInfoFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='format',
            location='query',
            required=False,
            type='string'
        ),
        coreapi.Field(
            name='site_code',
            location='query',
            required=True,
            type='string'
        )]


class VariablesFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='format',
            location='query',
            required=False,
            type='string'
        )]


class VariableInfoFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='format',
            location='query',
            required=False,
            type='string'
        ),
        coreapi.Field(
            name='variable_code',
            location='query',
            required=True,
            type='string'
        )]


class ValuesFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='format',
            location='query',
            required=False,
            type='string'
        ),
        coreapi.Field(
            name='site_code',
            location='query',
            required=True,
            type='string'
        ),
        coreapi.Field(
            name='variable_code',
            location='query',
            required=True,
            type='string'
        ),
        coreapi.Field(
            name='start_time',
            location='query',
            required=False,
            type='string'
        ),
        coreapi.Field(
            name='end_time',
            location='query',
            required=False,
            type='string'
        )]


class Refts(viewsets.ViewSet):

    def get_database_refts(self, request, network_id, database_id, *args, **kwaargs):
        """
        Builds a reference time series from a database.

        Rest URL Pattern:

        :param network: The network ID where the database is located.
        :param database: The database ID to build the REFTS from.
        """

        databases = {
            "odm2": wof_database_models.odm2.refts,
            "netcdf": wof_database_models.netcdf.refts
        }

        params = {
            "network": network_id,
            "database": database_id,
            "query_url": request.build_absolute_uri()
        }

        response = build_refts(databases, params)

        if response == "404_Not_Found":
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif response == "400_Bad_Request":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(response, status=status.HTTP_200_OK)


class Sites(viewsets.ViewSet):

    filter_backends = (SitesFilterBackend,)
    renderer_classes = (HydroServerRenderer,)

    def get_sites(self, request, network_id, database_id, *args, **kwargs):
        """
        Gets a list of available sites from a database.
        
        Rest URL Pattern: ~/wof/GetSites/?(network= # &database= # &format= # )

        :param network: The network ID where the database is located.
        :param database: The database ID to get sites from.
        :param format: The format of the response.
        """

        databases = {
            "odm2": wof_database_models.odm2.get_sites,
            "netcdf": wof_database_models.netcdf.get_sites
        }

        outputs = {
            "waterml": wof_output_models.waterml_1_1.get_sites,
            "waterjson": wof_output_models.waterjson_1_1.get_sites
        }

        params = {
            "network": network_id,
            "database": database_id,
            "format": request.GET.get("format"),
            "query_url": request.build_absolute_uri()
        }

        content_type = get_content_type(params["format"])

        response = get_wof_response(databases, outputs, params)

        if response == "404_Not_Found":
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif response == "400_Bad_Request":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status.HTTP_200_OK, content_type=content_type)


class SiteInfo(viewsets.ViewSet):

    filter_backends = (SiteInfoFilterBackend,)
    renderer_classes = (HydroServerRenderer,)

    def get_site_info(self, request, network_id, database_id, *args, **kwargs):
        """
        Gets information for a single site from a database.
        
        Rest URL Pattern: ~/wof/GetSiteInfo/?(network= # &database= # &format= # &site_code= # )

        :param network: The network ID where the database is located.
        :param database: The database ID to get the site info from.
        :param format: The format of the response.
        :param variable_code: The site code of the site of interest.
        """

        databases = {
            "odm2": wof_database_models.odm2.get_site_info,
            "netcdf": wof_database_models.netcdf.get_site_info
        }

        outputs = {
            "waterml": wof_output_models.waterml_1_1.get_site_info,
            "waterjson": wof_output_models.waterjson_1_1.get_site_info
        }

        params = {
            "network": network_id,
            "database": database_id,
            "format": request.GET.get("format"),
            "query_url": request.build_absolute_uri(),
            "site_code": request.GET.get("site_code")
        }

        content_type = get_content_type(params["format"])

        response = get_wof_response(databases, outputs, params)

        if response == "404_Not_Found":
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif response == "400_Bad_Request":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status.HTTP_200_OK, content_type=content_type)


class Variables(viewsets.ViewSet):

    filter_backends = (VariablesFilterBackend,)
    renderer_classes = (HydroServerRenderer,)

    def get_variables(self, request, network_id, database_id, *args, **kwargs):
        """
        Gets a list of available variables from a database.
        
        Rest URL Pattern: ~/wof/GetVariables/?(network= # &database= # &format= # )

        :param network: The network ID where the database is located.
        :param database: The database ID to get variables from.
        :param format: The format of the response.
        """

        print("HEY!!")

        databases = {
            "odm2": wof_database_models.odm2.get_variables,
            "netcdf": wof_database_models.netcdf.get_variables
        }

        outputs = {
            "waterml": wof_output_models.waterml_1_1.get_variables,
            "waterjson": wof_output_models.waterjson_1_1.get_variables
        }

        params = {
            "network": network_id,
            "database": database_id,
            "format": request.GET.get("format"),
            "query_url": request.build_absolute_uri()
        }

        content_type = get_content_type(params["format"])

        response = get_wof_response(databases, outputs, params)

        if response == "404_Not_Found":
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif response == "400_Bad_Request":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status.HTTP_200_OK, content_type=content_type)


class VariableInfo(viewsets.ViewSet):

    filter_backends = (VariableInfoFilterBackend,)
    renderer_classes = (HydroServerRenderer,)

    def get_variable_info(self, request, network_id, database_id, *args, **kwargs):
        """
        Gets information for a single variable from a database.
        
        Rest URL Pattern: ~/wof/GetVariableInfo/?(network= # &database= # &format= # &variable_code= # )

        :param network: The network ID where the database is located.
        :param database: The database ID to get the variable info from.
        :param format: The format of the response.
        :param variable_code: The variable code of the variable of interest.
        """

        databases = {
            "odm2": wof_database_models.odm2.get_variable_info,
            "netcdf": wof_database_models.netcdf.get_variable_info
        }

        outputs = {
            "waterml": wof_output_models.waterml_1_1.get_variable_info,
            "waterjson": wof_output_models.waterjson_1_1.get_variable_info
        }

        params = {
            "network": network_id,
            "database": database_id,
            "format": request.GET.get("format"),
            "query_url": request.build_absolute_uri(),
            "variable_code": request.GET.get("variable_code")
        }

        content_type = get_content_type(params["format"])

        response = get_wof_response(databases, outputs, params)

        if response == "404_Not_Found":
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif response == "400_Bad_Request":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status.HTTP_200_OK, content_type=content_type)


class Values(viewsets.ViewSet):

    filter_backends = (ValuesFilterBackend,)
    renderer_classes = (HydroServerRenderer,)

    def get_values(self, request, network_id, database_id, *args, **kwargs):
        """
        Gets time series values given a variable, site, start time, and end time.
        
        Rest URL Pattern: ~/wof/GetValues/?(network= # &database= # &format= # &site_code= # \
        &variable_code= # &start_time= # &end_time= #)

        :param network: The network ID where the database is located.
        :param database: The database ID to get time series values from.
        :param format: The format of the response.
        :param site_code: The site code used to obtain the time series values.
        :param variable_code: The variable code used to obtain the time series values.
        :param start_time: The start time of the time series.
        :param end_time: The end time of the time series.
        """

        databases = {
            "odm2": wof_database_models.odm2.get_values,
            "netcdf": wof_database_models.netcdf.get_values
        }

        outputs = {
            "waterml": wof_output_models.waterml_1_1.get_values,
            "waterjson": wof_output_models.waterjson_1_1.get_values
        }

        params = {
            "network": network_id,
            "database": database_id,
            "format": request.GET.get("format"),
            "query_url": request.build_absolute_uri(),
            "site_code": request.GET.get("site_code"),
            "variable_code": request.GET.get("variable_code"),
            "start_time": request.GET.get("start_time"),
            "end_time": request.GET.get("end_time")
        }

        content_type = get_content_type(params["format"])

        response = get_wof_response(databases, outputs, params)

        if response == "404_Not_Found":
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif response == "400_Bad_Request":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response, status.HTTP_200_OK, content_type=content_type)
