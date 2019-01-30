from rest_framework import serializers
from hydroserver_core.rest_api.models import Network, Database


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ('id', 'network_id')


class DatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database
        fields = ('id', 'network_id', 'database_id', 'database_name', 'database_path', 'database_type')
