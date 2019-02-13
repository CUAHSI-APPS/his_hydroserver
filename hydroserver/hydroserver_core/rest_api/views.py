from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework import viewsets, status
from hydroserver_core.rest_api.models import Network, Database
from hydroserver_core.rest_api.serializers import NetworkSerializer, DatabaseSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class Networks(viewsets.ViewSet):
    """
    Networks

    Test
    """

    permission_classes = (IsAuthenticated|ReadOnly,)

    def get_networks(self, request, *args, **kwargs):

        resources = Network.objects.all()
        serializer = NetworkSerializer(resources, many=True)

        return Response(serializer.data)

    def post_network(self, request, *args, **kwargs):

        serializer = NetworkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NetworkDetails(viewsets.ViewSet):
    """
    Network Details

    Test
    """

    permission_classes = (IsAuthenticated|ReadOnly,)

    def get_network_details(self, request, network_id, *args, **kwargs):

        try:
            network = Network.objects.get(network_id=network_id)
        except Network.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = NetworkSerializer(network)

        return Response(serializer.data)

    def delete_network(self, request, network_id, *args, **kwargs):

        try:
            network = Network.objects.get(network_id=network_id)
        except Network.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        databases = Database.objects.filter(network_id=network_id)

        databases.delete()
        network.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class Databases(viewsets.ViewSet):
    """
    Databases

    Test
    """

    permission_classes = (IsAuthenticated|ReadOnly,)

    def get_databases(self, request, network_id, *args, **kwargs):

        try:
            network = Network.objects.get(network_id=network_id)
        except Network.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        databases = Database.objects.filter(network_id=network_id).values()
        serializer = DatabaseSerializer(databases, many=True)

        return Response(serializer.data)

    def post_database(self, request, network_id, *args, **kwargs):

        #request.data.update({"network_id": network_id})
        serializer = DatabaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DatabaseDetails(viewsets.ViewSet):
    """
    Database Details

    Test
    """

    permission_classes = (IsAuthenticated|ReadOnly,)

    def get_database_details(self, request, network_id, database_id, *args, **kwargs):

        try:
            database = Database.objects.get(network_id=network_id, database_id=database_id)
        except Database.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DatabaseSerializer(database)

        return Response(serializer.data)

    def delete_database(self, request, network_id, database_id, *args, **kwargs):

        try:
            database = Database.objects.get(network_id=network_id, database_id=database_id)
        except Database.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        databases = Database.objects.filter(network_id=network_id)

        database.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
