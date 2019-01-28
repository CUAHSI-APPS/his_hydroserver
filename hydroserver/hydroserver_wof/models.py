import pandas as pd
from hydroserver_core.rest_api.serializers import DatabaseSerializer


class WofModels():

    query_table  = pd.DataFrame(columns = [
        "creation_time",
        "query_url",
        "method_called",
        "location_param",
        "variable_param",
        "begin_datetime",
        "end_datetime"
    ])

    site_info_table = pd.DataFrame(columns = [
        "site_code",
        "site_name",
        "latitude",
        "longitude",
        "elevation_m",
        "vertical_datum"
    ])

    series_catalog_table = pd.DataFrame(columns = [
        "value_count",
        "begin_datetime",
        "end_datetime"
    ])

    method_table = pd.DataFrame(columns = [
        "method_code",
        "method_description",
        "method_link"
    ])

    source_table = pd.DataFrame(columns= [
        "source_code",
        "organization",
        "source_description",
        "contact_name",
        "type_of_contact",
        "phone",
        "email",
        "address",
        "source_link"
    ])

    variable_info_table  = pd.DataFrame(columns = [
        "variable_code",
        "variable_name",
        "variable_description",
        "unit_name",
        "unit_abbreviation",
        "unit_code",
        "no_data_value"
    ])

    values_table = pd.DataFrame(columns = [
        "data_value",
        "date_time",
        "time_offset",
        "method_code",
        "source_code"
    ])
