from rest_framework import serializers
from hydroserver_core.models import Network, Database, Reference


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ("id", "network_id")


class DatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database
        fields = ("id", "network_id", "database_id", "database_name", "database_path", "database_type")


class ReferenceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Reference
		fields = ("id", "site_name", "site_code", "latitude", "longitude", "variable_name", "variable_code", "sample_medium", "value_count", "begin_date", "end_date", "method_link", "method_description", "network_id", "database_id")
