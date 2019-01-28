from rest_framework import serializers
from hydroserver_core.rest_api.models import Collection, Database


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'collection_id')


class DatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database
        fields = ('id', 'collection_id', 'database_id', 'database_name', 'database_path', 'database_type')
