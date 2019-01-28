from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework import viewsets, status
from hydroserver_core.rest_api.models import Collection, Database
from hydroserver_core.rest_api.serializers import CollectionSerializer, DatabaseSerializer


class Networks(viewsets.ViewSet):
    """
    Networks

    Test
    """

    def get_networks(self, request, *args, **kwargs):

        resources = Collection.objects.all()
        serializer = CollectionSerializer(resources, many=True)

        return Response(serializer.data)

    def post_network(self, request, *args, **kwargs):

        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NetworkDetails(viewsets.ViewSet):
    """
    Network Details

    Test
    """

    def get_network_details(self, request, network_id, *args, **kwargs):

        try:
            collection = Collection.objects.get(collection_id=network_id)
        except Collection.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionSerializer(collection)

        return Response(serializer.data)

    def delete_network(self, request, network_id, *args, **kwargs):

        try:
            collection = Collection.objects.get(collection_id=network_id)
        except Collection.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        databases = Database.objects.filter(collection_id=collection_id)

        databases.delete()
        collection.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class Databases(viewsets.ViewSet):
    """
    Databases

    Test
    """

    def get_databases(self, request, network_id, *args, **kwargs):

        try:
            collection = Collection.objects.get(collection_id=network_id)
        except Collection.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        databases = Database.objects.filter(collection_id=network_id).values()
        serializer = DatabaseSerializer(databases, many=True)

        return Response(serializer.data)

    def post_database(self, request, network_id, *args, **kwargs):

        request.data.update({"collection_id": network_id})
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

    def get_database_details(self, request, network_id, database_id, *args, **kwargs):

        try:
            database = Database.objects.get(collection_id=collection_id, database_id=database_id)
        except Database.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DatabaseSerializer(database)

        return Response(serializer.data)

    def delete_database(self, request, network_id, database_id, *args, **kwargs):

        try:
            database = Database.objects.get(collection_id=collection_id, database_id=database_id)
        except Database.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        databases = Database.objects.filter(collection_id=collection_id)

        database.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
