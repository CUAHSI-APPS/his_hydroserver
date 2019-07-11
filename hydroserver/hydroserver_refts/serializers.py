from rest_framework import serializers


class ReftsCatalogSerializer(serializers.Serializer):
	site_name = serializers.CharField(
		required=False,
		help_text="The site name for the timeseries."
	)
	site_code = serializers.CharField(
		required=False,
		help_text="The site code for the timeseries."
	)
	variable_name = serializers.CharField(
		required=False,
		help_text="The variable name for the timeseries."
	)
	variable_code = serializers.CharField(
		required=False,
		help_text="The variable code for the timeseries."
	)
	sample_medium = serializers.CharField(
		required=False,
		help_text="The sample medium for the timeseries."
	)
	method_link = serializers.CharField(
		required=False,
		help_text="The method link for the timeseries."
	)
	return_type = serializers.ChoiceField(
		required=False,
		help_text="The return type for the timeseries.",
		choices=[
			"WaterML 1.1",
			"WaterJSON 1.1"
		]
	)
	service_type = serializers.ChoiceField(
		required=False,
		help_text="The service type for the timeseries.",
		choices=[
			"REST"
		]
	)
	ref_type = serializers.ChoiceField(
		required=False,
		help_text="The reference type for the timeseries.",
		choices=[
			"WOF"
		]
	)
	min_value_count = serializers.IntegerField(
		required=False,
		help_text="The minimum value count for the timeseries.",
		min_value=0
	)
	max_value_count = serializers.IntegerField(
		required=False,
		help_text="The maximum value count for the timeseries.",
		min_value=0
	)
	start_date = serializers.DateTimeField(
		required=False,
		help_text="The minimum start date for the timeseries."
	)
	end_date = serializers.DateTimeField(
		required=False,
		help_text="The maximum end date for the timeseries."
	)
	north = serializers.FloatField(
		required=False,
		help_text="The north bound (maximum latitude) for the timeseries.",
		min_value=-90,
		max_value=90
	)
	south = serializers.FloatField(
		required=False,
		help_text="The south bound (minimum latitude) for the timeseries.",
		min_value=-90,
		max_value=90
	)
	east = serializers.FloatField(
		required=False,
		help_text="The east bound (maximum longitude) for the timeseries.",
		min_value=-180,
		max_value=180
	)
	west = serializers.FloatField(
		required=False,
		help_text="The west bound (minimum longitude) for the timeseries.",
		min_value=-180,
		max_value=180
	)
	network_id = serializers.CharField(
		required=False,
		help_text="The network id for the timeseries."
	)
	database_id = serializers.CharField(
		required=False,
		help_text="The database id for the timeseries."
	)


class ReftsParameterSerializer(serializers.Serializer):
    parameter = serializers.MultipleChoiceField(
        required=False,
        help_text="The parameters to get values for.",
        choices=[
            "site_name", 
            "site_code",
            "variable_name",
            "variable_code",
            "sample_medium",
            "method_link"
        ]
    )
