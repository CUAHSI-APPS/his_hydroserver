from rest_framework import serializers


class SiteInfoSerializer(serializers.Serializer):
    site_code = serializers.CharField(
        required=True,
        help_text="The site code to get a series catalog for."
    )


class VariableInfoSerializer(serializers.Serializer):
    variable_code = serializers.CharField(
        required=True,
        help_text="The variable code to get a series catalog for."
    )


class ValuesSerializer(serializers.Serializer):
    site_code = serializers.CharField(
        required=True,
        help_text="The site code to get a series catalog for."
    )
    variable_code = serializers.CharField(
        required=True,
        help_text="The variable code to get a series catalog for."
    )
    start_date = serializers.DateTimeField(
        required=False,
        help_text="The start date for the timeseries."
    )
    end_date = serializers.DateTimeField(
        required=False,
        help_text="The end date for the timeseries."
    )



