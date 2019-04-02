from rest_framework.response import Response
from rest_framework import viewsets, status
from hydroserver_core.rest_api.models import Network, Database
from hydroserver_core.rest_api.serializers import NetworkSerializer, DatabaseSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class NetworkRefts(viewsets.ViewSet):
    """
    Network REFTS

    Test
    """

    permission_classes = (IsAuthenticated|ReadOnly,)

    def get_network_refts(self, request, network_id, *args, **kwargs):

        try:
            network = Network.objects.get(network_id=network_id)
        except Network.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        databases = Database.objects.filter(network_id=network_id).values()
        serializer = DatabaseSerializer(databases, many=True)

        print(serializer.data)

        return Response(serializer.data)


class DatabaseRefts(viewsets.ViewSet):
    """
    Network REFTS

    Test
    """

    permission_classes = (IsAuthenticated|ReadOnly,)

    def get_database_refts(self, request, network_id, database_id, *args, **kwargs):

        try:
            database = Database.objects.get(network_id=network_id, database_id=database_id)
        except Database.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DatabaseSerializer(database)

        return Response(serializer.data)
