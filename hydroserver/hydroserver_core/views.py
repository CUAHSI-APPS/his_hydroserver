from rest_framework.response import Response
from rest_framework import viewsets, status
from hydroserver_core.models import Network as NetworkModel
from hydroserver_core.models import Database as DatabaseModel
from hydroserver_core.models import Reference as ReferenceModel
from hydroserver_core import core_database_models
from hydroserver_core.serializers import NetworkSerializer, DatabaseSerializer, ReferenceSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

from hydroserver import settings
from hydroserver_geospatial.utilities import create_workspace, delete_workspace, create_datastore, delete_datastore


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class Networks(viewsets.ModelViewSet):

    queryset = NetworkModel.objects.all()
    serializer_class = NetworkSerializer
    permission_classes = (IsAuthenticated|ReadOnly,)

    def get_networks(self, request, *args, **kwargs):
        """
        GET Networks

        Gets a list of networks available on the server.
        
        REST URL Pattern: ~/wds/manage/networks/
        
        """

        serializer = NetworkSerializer(NetworkModel.objects.all(), many=True)

        return Response(serializer.data)

    def post_network(self, request, *args, **kwargs):
        """
        POST Network

        Creates a new network.
        
        REST URL Pattern: ~/wds/networks/
        
        """

        serializer = NetworkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            if settings.CONNECT_GEOSERVER:
                create_workspace(request.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DatabaseList(viewsets.ModelViewSet):

    queryset = DatabaseModel.objects.all()
    serializer_class = DatabaseSerializer
    permission_classes = (IsAuthenticated|ReadOnly,)

    def get_database_list(self, request, *args, **kwargs):
        """
        GET Database List

        Gets a list of databases available on the server.

        REST URL Pattern: ~/wds/manage/database-list/

        """

        serializer = DatabaseSerializer(DatabaseModel.objects.all(), many=True)

        return Response(serializer.data)


class Network(viewsets.ModelViewSet):

    queryset = NetworkModel.objects.all()
    serializer_class = NetworkSerializer
    permission_classes = (IsAuthenticated|ReadOnly,)

    def get_network(self, request, network_id, *args, **kwargs):
        """
        GET Network

        Gets details for a network.
        
        REST URL Pattern: ~/wds/manage/network/

        :param network_id: Network ID of the network
        
        """

        try:
            network = NetworkModel.objects.get(network_id=network_id)
        except NetworkModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = NetworkSerializer(network)

        return Response(serializer.data)

    def delete_network(self, request, network_id, *args, **kwargs):
        """
        DELETE Network

        Deletes a network.
        
        REST URL Pattern: ~/wds/networks/

        :param network_id: Network ID of the network
        
        """

        try:
            network = NetworkModel.objects.get(network_id=network_id)
        except NetworkModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        databases = DatabaseModel.objects.filter(network_id=network_id)
        reference = ReferenceModel.objects.filter(network_id=network_id)

        reference.delete()
        databases.delete()
        network.delete()

        if settings.CONNECT_GEOSERVER:
            delete_workspace(network_id)

        return Response(status=status.HTTP_204_NO_CONTENT)


class Databases(viewsets.ModelViewSet):

    queryset = DatabaseModel.objects.all()
    serializer_class = DatabaseSerializer
    permission_classes = (IsAuthenticated|ReadOnly,)

    def get_databases(self, request, network_id, *args, **kwargs):
        """
        GET Databases

        Gets a list of databases available in a given network.
        
        REST URL Pattern: ~/wds/manage/networks/{network_id}/databases/

        :param network_id: Network ID of the network
        
        """

        try:
            network = NetworkModel.objects.get(network_id=network_id)
        except NetworkModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        databases = DatabaseModel.objects.filter(network_id=network_id).values()
        serializer = DatabaseSerializer(databases, many=True)

        return Response(serializer.data)

    def post_database(self, request, network_id, *args, **kwargs):
        """
        POST Database

        Creates a new database.
        
        REST URL Pattern: ~/wds/manage/network/{network_id}/databases/

        :param network_id: Network ID of the network
        
        """

        serializer = DatabaseSerializer(data=request.data)
        if serializer.is_valid():

            database_type = request.data["database_type"]
            database_id = request.data["database_id"]
            database_path = request.data["database_path"]

            databases = {
                "odm2_sqlite": core_database_models.odm2_sqlite.get_catalog_info
            }

            if not databases.get(database_type):
                return Response(status=status.HTTP_400_BAD_REQUEST)

            reference_table = databases[database_type](network=network_id, database=database_id, database_path=database_path)

            if str(reference_table) == "400_Bad_Request":
                return Response(status=status.HTTP_400_BAD_REQUEST)

            reference_data = [{
                    "site_name": i[3], 
                    "site_code": i[4], 
                    "latitude": i[5], 
                    "longitude": i[6], 
                    "variable_name": i[7], 
                    "variable_code": i[8], 
                    "sample_medium": i[1], 
                    "value_count": i[2], 
                    "begin_date": i[11], 
                    "end_date": i[12], 
                    "method_link": i[9], 
                    "method_description": i[10], 
                    "network_id": network_id, 
                    "database_id": database_id
                } for i in reference_table.itertuples(index=True, name="Pandas")]

            if len(reference_data) > 1:
                many = True
            else:
                reference_data = reference_data[0]
                many = False

            reference_serializer = ReferenceSerializer(data=reference_data, many=many)
            if reference_serializer.is_valid():
                serializer.save()
                reference_serializer.save()

                if settings.CONNECT_GEOSERVER:
                    create_datastore(reference_data, many)

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(reference_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Database(viewsets.ModelViewSet):

    queryset = DatabaseModel.objects.all()
    serializer_class = DatabaseSerializer
    permission_classes = (IsAuthenticated|ReadOnly,)

    def get_database(self, request, network_id, database_id, *args, **kwargs):
        """
        GET Database

        Gets database details.
        
        REST URL Pattern: ~/wds/manage/network/{network_id}/databases/{database_id}/

        :param network_id: Network ID of the network
        :param database_id: Database ID of the database
        
        """

        try:
            database = DatabaseModel.objects.get(network_id=network_id, database_id=database_id)
        except DatabaseModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DatabaseSerializer(database)

        return Response(serializer.data)

    def delete_database(self, request, network_id, database_id, *args, **kwargs):
        """
        DELETE Database

        Deletes a database.
        
        REST URL Pattern: ~/wds/manage/network/{network_id}/databases/{database_id}/

        :param network_id: Network ID of the network
        :param database_id: Database ID of the database
        
        """

        try:
            database = DatabaseModel.objects.get(network_id=network_id, database_id=database_id)
        except DatabaseModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        reference = ReferenceModel.objects.filter(network_id=network_id, database_id=database_id)

        database.delete()
        reference.delete()

        if settings.CONNECT_GEOSERVER:
            delete_datastore(network_id, database_id)

        return Response(status=status.HTTP_204_NO_CONTENT)
