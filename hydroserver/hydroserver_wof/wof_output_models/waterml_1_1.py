import pandas as pd
from hydroserver_wof.models import WofModels
from xml.sax.saxutils import escape, unescape


def e(text):
    if isinstance(text, str): 
        return escape(unescape(text))
    else:
        return text


def query_url_(query_url):
    return (
        f'<queryURL>'
        f'{e(query_url)}'
        f'</queryURL>'
    )


def begin_datetime_(begin_datetime):
    return (
        f'<beginDateTime>'
        f'{e(begin_datetime)}'
        f'</beginDateTime>'
    )


def end_datetime_(end_datetime):
    return (
        f'<endDateTime>'
        f'{e(end_datetime)}'
        f'</endDateTime>'
    )


def time_param_(begin_datetime, end_datetime):
    return (
        f'<timeParam>'
        f'{begin_datetime_(begin_datetime) if begin_datetime else ""}'
        f'{end_datetime_(end_datetime) if end_datetime else ""}'
        f'</timeParam>'
    )


def variable_param_(variable_param):
    return (
        f'<variableParam>'
        f'{e(variable_param)}'
        f'</variableParam>'
    )


def location_param_(location_param):
    return (
        f'<locationParam>'
        f'{e(location_param)}'
        f'</locationParam>'
    )


def criteria_(method_called, location_param, variable_param, begin_datetime, end_datetime):
    return (
        f'<criteria MethodCalled="{method_called}">'
        f'{location_param_(location_param) if location_param else ""}'
        f'{variable_param_(variable_param) if variable_param else ""}'
        f'{time_param_(begin_datetime, end_datetime) if any((begin_datetime, end_datetime)) else ""}'
        f'</criteria>'
    )


def creation_time_(creation_time):
    return (
        f'<creationTime>'
        f'{e(creation_time)}'
        f'</creationTime>'
    )


def query_info_(creation_time, query_url, method_called, location_param, variable_param, begin_datetime, end_datetime):
    return (
        f'<queryInfo>'
        f'{creation_time_(creation_time) if creation_time else ""}'
        f'{query_url_(query_url) if query_url else ""}'
        f'{criteria_(method_called, location_param, variable_param, begin_datetime, end_datetime) if any((method_called, location_param, variable_param, begin_datetime, end_datetime)) else ""}'
        f'</queryInfo>'
    )


def site_code_(site_code):
    return (
        f'<siteCode network="default">'
        f'{e(site_code)}'
        f'</siteCode>'
    )


def site_name_(site_name):
    return (
        f'<siteName>'
        f'{e(site_name)}'
        f'</siteName>'
    )


def latitude_(latitude):
    return (
        f'<latitude>'
        f'{e(latitude)}'
        f'</latitude>'
    )


def longitude_(longitude):
    return (
        f'<longitude>'
        f'{e(longitude)}'
        f'</longitude>'
    )


def geog_location_(latitude, longitude):
    return (
        f'<geogLocation xsi:type="LatLonPointType">'
        f'{latitude_(latitude)}'
        f'{longitude_(longitude)}'
        f'</geogLocation>'
    )


def geolocation_(latitude, longitude):
    return (
        f'<geoLocation>'
        f'{geog_location_(latitude, longitude)}'
        f'</geoLocation>'
    )


def elevation_m_(elevation_m):
    return (
        f'<elevation_m>'
        f'{e(elevation_m)}'
        f'</elevation_m>'
    )


def vertical_datum_(vertical_datum):
    return (
        f'<verticalDatum>'
        f'{e(vertical_datum)}'
        f'</verticalDatum>'
    )


def site_info_(site_code, site_name, latitude, longitude, elevation_m, vertical_datum):
    return (
        f'<siteInfo>'
        f'{site_name_(site_name) if site_name else ""}'
        f'{site_code_(site_code) if site_code else ""}'
        f'{geolocation_(latitude, longitude) if all((latitude, longitude)) else ""}'
        f'{elevation_m_(elevation_m) if elevation_m else ""}'
        f'{vertical_datum_(vertical_datum) if vertical_datum else ""}'
        f'</siteInfo>'
    )


def source_info_(site_code, site_name, latitude, longitude, elevation_m, vertical_datum):
    return (
        f'<sourceInfo xsi:type="SiteInfoType">'
        f'{site_name_(site_name) if site_name else ""}'
        f'{site_code_(site_code) if site_code else ""}'
        f'{geolocation_(latitude, longitude) if all((latitude, longitude)) else ""}'
        f'{elevation_m_(elevation_m) if elevation_m else ""}'
        f'{vertical_datum_(vertical_datum) if vertical_datum else ""}'
        f'</sourceInfo>'
    )


def variable_code_(variable_code):
    return (
        f'<variableCode>'
        f'{e(variable_code)}'
        f'</variableCode>'
    )


def variable_name_(variable_name):
    return (
        f'<variableName>'
        f'{e(variable_name)}'
        f'</variableName>'
    )


def variable_description_(variable_description):
    return (
        f'<variableDescription>'
        f'{e(variable_description)}'
        f'</variableDescription>'
    )


def unit_(unit_name, unit_abbreviation, unit_code):
    return (
        f'<unit>'
        f'{unit_name_(unit_name) if unit_name else ""}'
        f'{unit_abbreviation_(unit_abbreviation) if unit_abbreviation else ""}'
        f'{unit_code_(unit_code) if unit_code else ""}'
        f'</unit>'
    )


def unit_name_(unit_name):
    return (
        f'<unitName>'
        f'{e(unit_name)}'
        f'</unitName>'
    )


def unit_abbreviation_(unit_abbreviation):
    return (
        f'<unitAbbreviation>'
        f'{e(unit_abbreviation)}'
        f'</unitAbbreviation>'
    )


def unit_code_(unit_code):
    return (
        f'<unitCode>'
        f'{e(unit_code)}'
        f'</unitCode>'
    )


def no_data_value_(no_data_value):
    return (
        f'<noDataValue>'
        f'{e(no_data_value)}'
        f'</noDataValue>'
    )


def value_count_(value_count):
    return (
        f'<valueCount>'
        f'{e(value_count)}'
        f'</valueCount>'
    )


def variable_(variable_code, variable_name, variable_description, unit_name, unit_abbreviation, unit_code, no_data_value):
    return (
        f'<variable>'
        f'{variable_code_(variable_code) if variable_code else ""}'
        f'{variable_name_(variable_name) if variable_name else ""}'
        f'{variable_description_(variable_description) if variable_description else ""}'
        f'{unit_(unit_name, unit_abbreviation, unit_code) if any((unit_name, unit_abbreviation, unit_code)) else ""}'
        f'{no_data_value_(no_data_value) if no_data_value else ""}'
        f'</variable>'
    )


def variable_time_interval_(begin_datetime, end_datetime):
    return (
        f'<variableTimeInterval>'
        f'{begin_datetime_(begin_datetime) if begin_datetime else ""}'
        f'{end_datetime_(end_datetime) if end_datetime else ""}'
        f'</variableTimeInterval>'
    )


def method_(method_code, method_description, method_link):
    return (
        f'<method>'
        f'{method_code_(method_code) if method_code else ""}'
        f'{method_description_(method_description) if method_description else ""}'
        f'{method_link_(method_link) if method_link else ""}'
        f'</method>'
    )


def method_code_(method_code):
    return (
        f'<methodCode>'
        f'{e(method_code)}'
        f'</methodCode>'
    )


def method_description_(method_description):
    return (
        f'<methodDescription>'
        f'{e(method_description)}'
        f'</methodDescription>'
    )


def method_link_(method_link):
    return (
        f'<methodLink>'
        f'{e(method_link)}'
        f'</methodLink>'
    )


def source_code_(source_code):
    return (
        f'<sourceCode>'
        f'{e(source_code)}'
        f'</sourceCode>'
    )


def organization_(organization):
    return (
        f'<organization>'
        f'{e(organization)}'
        f'</organization>'
    )


def source_description_(source_description):
    return (
        f'<sourceDescription>'
        f'{e(source_description)}'
        f'</sourceDescription>'
    )


def source_link_(source_link):
    return (
        f'<sourceLink>'
        f'{e(source_link)}'
        f'</sourceLink>'
    )


def contact_name_(contact_name):
    return (
        f'<contactName>'
        f'{e(contact_name)}'
        f'</contactName>'
    )


def type_of_contact_(type_of_contact):
    return (
        f'<typeOfContact>'
        f'{e(type_of_contact)}'
        f'</typeOfContact>'
    )


def phone_(phone):
    return (
        f'<phone>'
        f'{e(phone)}'
        f'</phone>'
    )


def email_(email):
    return (
        f'<email>'
        f'{e(email)}'
        f'</email>'
    )


def address_(address):
    return (
        f'<address>'
        f'{e(address)}'
        f'</address>'
    )


def contact_information_(contact_name, type_of_contact, phone, email, address):
    return (
        f'<contactInformation>'
        f'{contact_name_(contact_name) if contact_name else ""}'
        f'{type_of_contact_(type_of_contact) if type_of_contact else ""}'
        f'{email_(email) if email else ""}'
        f'{phone_(phone) if phone else ""}'
        f'{address_(address) if address else ""}'
        f'</contactInformation>'
    )


def source_(source_code, organization, source_description, contact_name, type_of_contact, phone, email, address, source_link):
    return(
        f'<source>'
        f'{source_code_(source_code) if source_code else ""}'
        f'{organization_(organization) if organization else ""}'
        f'{source_description_(source_description) if source_description else ""}'
        f'{contact_information_(contact_name, type_of_contact, phone, email, address) if any((contact_name, type_of_contact, phone, email, address)) else ""}'
        f'{source_link_(source_link) if source_link else ""}'
        f'</source>'
    )


def series_(value_count, begin_datetime, end_datetime, variable_code, variable_name, variable_description, unit_name, unit_abbreviation, unit_code, no_data_value, method_code, method_description, method_link, source_code, organization, source_description, contact_name, type_of_contact, phone, email, address, source_link):
    return (
        f'<series>'
        f'{variable_(variable_code, variable_name, variable_description, unit_name, unit_abbreviation, unit_code, no_data_value) if any((variable_code, variable_name, variable_description, unit_name, unit_abbreviation, unit_code, no_data_value)) else ""}'
        f'{value_count_(value_count) if value_count else None}'
        f'{variable_time_interval_(begin_datetime, end_datetime) if any((begin_datetime, end_datetime)) else ""}'
        f'{method_(method_code, method_description, method_link) if any((method_code, method_description, method_link)) else ""}'
        f'{source_(source_code, organization, source_description, contact_name, type_of_contact, phone, email, address, source_link) if any((source_code, organization, source_description, contact_name, type_of_contact, phone, email, address, source_link)) else ""}'
        f'</series>'
    )


def series_catalog_(series_catalog_table):
    return (
        f'<seriesCatalog>'
        f'{"".join(series_(series[1], series[2], series[3], series[4], series[5], series[6], series[7], series[8], series[9], series[10], series[11], series[12], series[13], series[14], series[15], series[16], series[17], series[18], series[19], series[20], series[21], series[22]) for series in series_catalog_table.itertuples(index=True, name="Pandas")) if series_catalog_table is not None else ""}'
        f'</seriesCatalog>'
    )


def site_(site_code, site_name, latitude, longitude, elevation_m, vertical_datum, series_catalog_table=None):
    return (
        f'<site>'
        f'{site_info_(site_code, site_name, latitude, longitude, elevation_m, vertical_datum) if any((site_code, site_name, latitude, longitude, elevation_m, vertical_datum)) else ""}'
        f'{series_catalog_(series_catalog_table) if series_catalog_table is not None else ""}'
        f'</site>'
    )


def variables_(variable_info_table):
    return (
        f'<variables>'
        f'{"".join(variable_(variable[1], variable[2], variable[3], variable[4], variable[5], variable[6], variable[7]) for variable in variable_info_table.itertuples(index=True, name="Pandas")) if variable_info_table is not None else ""}'
        f'</variables>'
    )


def value_(data_value, date_time, time_offset, method_id, source_id):
    time_offset_attr = f' timeOffset="{e(time_offset)}"' if time_offset is not None else ""
    method_code_attr = f' methodCode="{e(method_id)}"' if method_id is not None else ""
    source_code_attr = f' sourceCode="{e(source_id)}"' if source_id is not None else ""
    return (
        f'<value'
        f' dateTime="{e(date_time)}"'
        f'{time_offset_attr}'
        f'{method_code_attr}'
        f'{source_code_attr}'
        f'>{e(data_value)}</value>'
    )


def values_(values_table, method_table, source_table):
    return (
        f'<values>'
        f'{"".join(value_(value[1], value[2], value[3], value[4], value[5]) for value in values_table.itertuples(index=True, name="Pandas")) if values_table is not None else ""}'
        f'{"".join(method_(method[1], method[2], method[3]) for method in method_table.itertuples(index=True, name="Pandas")) if method_table is not None else ""}'
        f'{"".join(source_(source[1], source[2], source[3], source[4], source[5], source[6], source[7], source[8], source[9]) for source in source_table.itertuples(index=True, name="Pandas")) if source_table is not None else ""}'
        f'</values>'
    )


def time_series_(site_info_table, variable_info_table, values_table, method_table, source_table):
    return (
        f'<timeSeries>'
        f'{"".join(source_info_(site[1], site[2], site[3], site[4], site[5], site[6]) for site in site_info_table.itertuples(index=True, name="Pandas")) if site_info_table is not None else ""}'
        f'{"".join(variable_(variable[1], variable[2], variable[3], variable[4], variable[5], variable[6], variable[7]) for variable in variable_info_table.itertuples(index=True, name="Pandas")) if variable_info_table is not None else ""}'
        f'{values_(values_table, method_table, source_table) if any((values_table is not None, method_table is not None, source_table is not None)) else ""}'
        f'</timeSeries>'
    )


def get_variables(output_data):

    query_table = output_data["query_table"]
    variable_info_table = output_data["variable_info_table"]

    response = (
        f'<variablesResponse xmlns="http://www.cuahsi.org/waterML/1.1/">'
        f'{"".join(query_info_(query[1], query[2], query[3], query[4], query[5], query[6], query[7]) for query in query_table.itertuples(index=True, name="Pandas")) if query_table is not None else ""}'
        f'{variables_(variable_info_table) if variable_info_table is not None else ""}'
        f'</variablesResponse>'
    )

    return response


def get_site_info(output_data):

    query_table = output_data["query_table"]
    site_info_table = output_data["site_info_table"]
    variable_info_table = output_data["variable_info_table"] if output_data["variable_info_table"] is not None else WofModels.variable_info_table.append(pd.DataFrame([tuple(None for i in WofModels.variable_info_table.columns)], columns=WofModels.variable_info_table.columns))
    series_catalog_table = output_data["series_catalog_table"] if output_data["series_catalog_table"] is not None else WofModels.series_catalog_table.append(pd.DataFrame([tuple(None for i in WofModels.series_catalog_table.columns)], columns=WofModels.series_catalog_table.columns))
    method_table = output_data["method_table"] if output_data["method_table"] is not None else WofModels.method_table.append(pd.DataFrame([tuple(None for i in WofModels.method_table.columns)], columns=WofModels.method_table.columns))
    source_table = output_data["source_table"] if output_data["source_table"] is not None else WofModels.source_table.append(pd.DataFrame([tuple(None for i in WofModels.source_table.columns)], columns=WofModels.source_table.columns))

    series_catalog_table = pd.concat([series_catalog_table, variable_info_table, method_table, source_table], axis=1, ignore_index=True)

    response = (
        f'<sitesResponse xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.cuahsi.org/waterML/1.1/">'
        f'{"".join(query_info_(query[1], query[2], query[3], query[4], query[5], query[6], query[7]) for query in query_table.itertuples(index=True, name="Pandas")) if query_table is not None else ""}'
        f'{"".join(site_(site[1], site[2], site[3], site[4], site[5], site[6], series_catalog_table) for site in site_info_table.itertuples(index=True, name="Pandas")) if site_info_table is not None else ""}'
        f'</sitesResponse>'
    )

    return response


def get_sites(output_data):

    query_table = output_data["query_table"]
    site_info_table = output_data["site_info_table"]

    response = (
        f'<sitesResponse xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.cuahsi.org/waterML/1.1/">'
        f'{"".join(query_info_(query[1], query[2], query[3], query[4], query[5], query[6], query[7]) for query in query_table.itertuples(index=True, name="Pandas")) if query_table is not None else ""}'
        f'{"".join(site_(site[1], site[2], site[3], site[4], site[5], site[6]) for site in site_info_table.itertuples(index=True, name="Pandas")) if site_info_table is not None else ""}'
        f'</sitesResponse>'
    )

    return response


def get_variable_info(output_data):

    query_table = output_data["query_table"]
    variable_info_table = output_data["variable_info_table"]

    response = (
        f'<variablesResponse xmlns="http://www.cuahsi.org/waterML/1.1/">'
        f'{"".join(query_info_(query[1], query[2], query[3], query[4], query[5], query[6], query[7]) for query in query_table.itertuples(index=True, name="Pandas")) if query_table is not None else ""}'
        f'{variables_(variable_info_table) if variable_info_table is not None else ""}'
        f'</variablesResponse>'
    )

    return response


def get_values(output_data):

    query_table = output_data["query_table"]
    site_info_table = output_data["site_info_table"]
    variable_info_table = output_data["variable_info_table"]
    values_table = output_data["values_table"]
    method_table = output_data["method_table"]
    source_table = output_data["source_table"]

    response = (
        f'<timeSeriesResponse xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.cuahsi.org/waterML/1.1/">'
        f'{"".join(query_info_(query[1], query[2], query[3], query[4], query[5], query[6], query[7]) for query in query_table.itertuples(index=True, name="Pandas")) if query_table is not None else ""}'
        f'{"".join(time_series_(site_info_table, variable_info_table, values_table, method_table, source_table)) if any((site_info_table is not None, variable_info_table is not None, values_table is not None, method_table is not None, source_table is not None)) else ""}'
        f'</timeSeriesResponse>'
    )

    return response
