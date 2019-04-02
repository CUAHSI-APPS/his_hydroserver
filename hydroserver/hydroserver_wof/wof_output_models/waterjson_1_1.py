import pandas as pd
import json
from hydroserver_wof.models import WofModels


def time_param_(begin_datetime, end_datetime):

    time_param = {}

    time_param.update({"beginDateTime": begin_datetime} if begin_datetime else {})
    time_param.update({"endDateTime": end_datetime} if end_datetime else {})

    return time_param


def criteria_(method_called, location_param, variable_param, begin_datetime, end_datetime):

    criteria = {}

    time_param = time_param_(begin_datetime, end_datetime)

    criteria.update({"MethodCalled": method_called} if method_called else {})
    criteria.update({"locationParam": location_param} if location_param else {})
    criteria.update({"variableParam": variable_param} if variable_param else {})
    criteria.update({"timeParam": time_param} if time_param else {})

    return criteria


def query_info_(creation_time, query_url, method_called, location_param, variable_param, begin_datetime, end_datetime):

    query_info = {}

    criteria = criteria_(method_called, location_param, variable_param, begin_datetime, end_datetime)

    query_info.update({"creationTime": creation_time} if creation_time else {})
    query_info.update({"queryURL": query_url} if query_url else {})
    query_info.update({"criteria": criteria} if criteria else {})

    return query_info


def geog_location_(latitude, longitude):

    geog_location = {}

    geog_location.update({"latitude": latitude} if latitude else {})
    geog_location.update({"longitude": longitude} if longitude else {})

    return geog_location


def geolocation_(latitude, longitude):

    geo_location = {}

    geog_location = geog_location_(latitude, longitude)

    geo_location.update({"geogLocation": geog_location} if geog_location else {})

    return geo_location


def site_info_(site_code, site_name, latitude, longitude, elevation_m, vertical_datum):

    site_info = {}

    geo_location = geolocation_(latitude, longitude)

    site_info.update({"siteCode": site_code} if site_code else {})
    site_info.update({"siteName": site_name} if site_name else {})
    site_info.update({"geoLocation": geo_location} if geo_location else {})
    site_info.update({"elevation_m": elevation_m} if elevation_m else {})
    site_info.update({"verticalDatum": vertical_datum} if vertical_datum else {})    

    return site_info


def source_info_(site_code, site_name, latitude, longitude, elevation_m, vertical_datum):

    source_info = {}

    geo_location = geolocation_(latitude, longitude)

    source_info.update({"siteCode": site_code} if site_code else {})
    source_info.update({"siteName": site_name} if site_name else {})
    source_info.update({"geoLocation": geo_location} if geo_location else {})
    source_info.update({"elevation_m": elevation_m} if elevation_m else {})
    source_info.update({"verticalDatum": vertical_datum} if vertical_datum else {})    

    return source_info


def unit_(unit_name, unit_abbreviation, unit_code):

    unit = {}

    unit.update({"unitName": unit_name} if unit_name else {})
    unit.update({"unitAbbreviation": unit_abbreviation} if unit_abbreviation else {})
    unit.update({"unitCode": unit_code} if unit_code else {})

    return unit


def variable_(variable_code, variable_name, variable_description, unit_name, unit_abbreviation, unit_code, no_data_value):

    variable = {}

    unit = unit_(unit_name, unit_abbreviation, unit_code)

    variable.update({"variableCode": variable_code} if variable_code else {})
    variable.update({"variableName": variable_name} if variable_name else {})
    variable.update({"variableDescription": variable_description} if variable_description else {})
    variable.update({"unit": unit} if unit else {})
    variable.update({"noDataValue": no_data_value} if no_data_value else {})

    return variable


def variable_time_interval_(begin_datetime, end_datetime):

    variable_time_interval = {}

    variable_time_interval.update({"beginDateTime": begin_datetime} if begin_datetime else {})
    variable_time_interval.update({"endDateTime": end_datetime} if end_datetime else {})

    return variable_time_interval


def method_(method_code, method_description, method_link):

    method = {}

    method.update({"methodCode": method_code} if method_code else {})
    method.update({"methodDescription": method_description} if method_description else {})
    method.update({"methodLink": method_link} if method_link else {})

    return method


def contact_information_(contact_name, type_of_contact, phone, email, address):

    contact_information = {}

    contact_information.update({"contactName": contact_name} if contact_name else {})
    contact_information.update({"typeOfContact": type_of_contact} if type_of_contact else {})
    contact_information.update({"email": email} if email else {})
    contact_information.update({"phone": phone} if phone else {})
    contact_information.update({"address": address} if address else {})

    return contact_information


def source_(source_code, organization, source_description, contact_name, type_of_contact, phone, email, address, source_link):

    source = {}

    contact_information = contact_information_(contact_name, type_of_contact, phone, email, address)

    source.update({"sourceCode": source_code} if source_code else {})
    source.update({"organization": organization} if organization else {})
    source.update({"sourceDescription": source_description} if source_description else {})
    source.update({"contactInformation": contact_information} if contact_information else {})
    source.update({"sourceLink": source_link} if source_link else {})

    return source


def series_(value_count, begin_datetime, end_datetime, variable_code, variable_name, variable_description, unit_name, unit_abbreviation, unit_code, no_data_value, method_code, method_description, method_link, source_code, organization, source_description, contact_name, type_of_contact, phone, email, address, source_link):

    series = {}

    variable = variable_(variable_code, variable_name, variable_description, unit_name, unit_abbreviation, unit_code, no_data_value)
    variable_time_interval = variable_time_interval_(begin_datetime, end_datetime)
    method = method_(method_code, method_description, method_link)
    source = source_(source_code, organization, source_description, contact_name, type_of_contact, phone, email, address, source_link)

    series.update({"variable": variable} if variable else {})
    series.update({"valueCount": value_count} if value_count else {})
    series.update({"variableTimeInterval": variable_time_interval} if variable_time_interval else {})
    series.update({"method": method} if method else {})
    series.update({"source": source} if source else {})

    return series


def site_(site_code, site_name, latitude, longitude, elevation_m, vertical_datum, series_catalog_table=None):

    site = {}

    site_info = site_info_(site_code, site_name, latitude, longitude, elevation_m, vertical_datum)
    series_catalog = [{"series": series_(series[1], series[2], series[3], series[4], series[5], series[6], series[7], series[8], series[9], series[10], series[11], series[12], series[13], series[14], series[15], series[16], series[17], series[18], series[19], series[20], series[21], series[22])} for series in series_catalog_table.itertuples(index=True, name="Pandas")] if series_catalog_table is not None else None

    site.update({"siteInfo": site_info} if site_info else {})
    site.update({"seriesCatalog": series_catalog} if series_catalog is not None else {})

    return site


def value_(data_value, date_time, time_offset, method_id, source_id):

    value = {}

    value.update({"dataValue": data_value} if data_value else {})
    value.update({"dateTime": date_time} if date_time else {})
    value.update({"timeOffset": time_offset} if time_offset else {})
    value.update({"methodCode": method_id} if method_id else {})
    value.update({"sourceCode": source_id} if source_id else {})

    return value


def time_series_(site_info_table, variable_info_table, values_table, method_table, source_table):

    time_series = {}

    source_info = next(iter([source_info_(site[1], site[2], site[3], site[4], site[5], site[6]) for site in site_info_table.itertuples(index=True, name="Pandas")]), None) if site_info_table is not None else None
    variable = next(iter([variable_(variable[1], variable[2], variable[3], variable[4], variable[5], variable[6], variable[7]) for variable in variable_info_table.itertuples(index=True, name="Pandas")]), None) if variable_info_table is not None else None
    methods = [{"method": method_(method[1], method[2], method[3])} for method in method_table.itertuples(index=True, name="Pandas")] if method_table is not None else None
    sources = [{"source": source_(source[1], source[2], source[3], source[4], source[5], source[6], source[7], source[8], source[9])} for source in source_table.itertuples(index=True, name="Pandas")] if source_table is not None else None
    values = [{"value": value_(value[1], value[2], value[3], value[4], value[5])} for value in values_table.itertuples(index=True, name="Pandas")] if values_table is not None else None

    time_series.update({"sourceInfo": source_info} if source_info else {})
    time_series.update({"variable": variable} if variable else {})
    time_series.update({"methods": methods} if methods else {})
    time_series.update({"sources": sources} if sources else {})
    time_series.update({"values": values} if values else {})

    return time_series


def get_variables(output_data):

    query_table = output_data["query_table"]
    variable_info_table = output_data["variable_info_table"]

    variables_response = {}

    query_info = next(iter([query_info_(query[1], query[2], query[3], query[4], query[5], query[6], query[7]) for query in query_table.itertuples(index=True, name="Pandas")]), None) if query_table is not None else None
    variables = [{"variable": variable_(variable[1], variable[2], variable[3], variable[4], variable[5], variable[6], variable[7])} for variable in variable_info_table.itertuples(index=True, name="Pandas")] if variable_info_table is not None else None

    variables_response.update({"queryInfo": query_info} if query_info else {})
    variables_response.update({"variables": variables} if variables else {})

    response = {"variablesResponse": variables_response}

    return json.dumps(response)


def get_site_info(output_data):

    query_table = output_data["query_table"]
    site_info_table = output_data["site_info_table"]
    variable_info_table = output_data["variable_info_table"] if output_data["variable_info_table"] is not None else WofModels.variable_info_table.append(pd.DataFrame([tuple(None for i in WofModels.variable_info_table.columns)], columns=WofModels.variable_info_table.columns))
    series_catalog_table = output_data["series_catalog_table"] if output_data["series_catalog_table"] is not None else WofModels.series_catalog_table.append(pd.DataFrame([tuple(None for i in WofModels.series_catalog_table.columns)], columns=WofModels.series_catalog_table.columns))
    method_table = output_data["method_table"] if output_data["method_table"] is not None else WofModels.method_table.append(pd.DataFrame([tuple(None for i in WofModels.method_table.columns)], columns=WofModels.method_table.columns))
    source_table = output_data["source_table"] if output_data["source_table"] is not None else WofModels.source_table.append(pd.DataFrame([tuple(None for i in WofModels.source_table.columns)], columns=WofModels.source_table.columns))

    sites_response = {}

    series_catalog_table = pd.concat([series_catalog_table, variable_info_table, method_table, source_table], axis=1, ignore_index=True)

    query_info = next(iter([query_info_(query[1], query[2], query[3], query[4], query[5], query[6], query[7]) for query in query_table.itertuples(index=True, name="Pandas")]), None) if query_table is not None else None
    sites = [{"site": site_(site[1], site[2], site[3], site[4], site[5], site[6], series_catalog_table)} for site in site_info_table.itertuples(index=True, name="Pandas")] if site_info_table is not None else None

    sites_response.update({"queryInfo": query_info} if query_info else {})
    sites_response.update({"sites": sites} if sites else {})

    response = {"sitesResponse": sites_response}

    return json.dumps(response)


def get_sites(output_data):

    query_table = output_data["query_table"]
    site_info_table = output_data["site_info_table"]

    sites_response = {}

    query_info = next(iter([query_info_(query[1], query[2], query[3], query[4], query[5], query[6], query[7]) for query in query_table.itertuples(index=True, name="Pandas")]), None) if query_table is not None else None
    sites = [{"site": site_(site[1], site[2], site[3], site[4], site[5], site[6], None)} for site in site_info_table.itertuples(index=True, name="Pandas")] if site_info_table is not None else None

    sites_response.update({"queryInfo": query_info} if query_info else {})
    sites_response.update({"sites": sites} if sites else {})

    response = {"sitesResponse": sites_response}

    return json.dumps(response)


def get_variable_info(output_data):

    query_table = output_data["query_table"]
    variable_info_table = output_data["variable_info_table"]

    variables_response = {}

    query_info = next(iter([query_info_(query[1], query[2], query[3], query[4], query[5], query[6], query[7]) for query in query_table.itertuples(index=True, name="Pandas")]), None) if query_table is not None else None
    variables = [{"variable": variable_(variable[1], variable[2], variable[3], variable[4], variable[5], variable[6], variable[7])} for variable in variable_info_table.itertuples(index=True, name="Pandas")] if variable_info_table is not None else None

    variables_response.update({"queryInfo": query_info} if query_info else {})
    variables_response.update({"variables": variables} if variables else {})

    response = {"variablesResponse": variables_response}

    return json.dumps(response)


def get_values(output_data):

    query_table = output_data["query_table"]
    site_info_table = output_data["site_info_table"]
    variable_info_table = output_data["variable_info_table"]
    values_table = output_data["values_table"]
    method_table = output_data["method_table"]
    source_table = output_data["source_table"]

    timeseries_response = {}

    query_info = next(iter([query_info_(query[1], query[2], query[3], query[4], query[5], query[6], query[7]) for query in query_table.itertuples(index=True, name="Pandas")]), None) if query_table is not None else None
    time_series = time_series_(site_info_table, variable_info_table, values_table, method_table, source_table)

    timeseries_response.update({"queryInfo": query_info} if query_info else {})
    timeseries_response.update({"timeSeries": time_series} if time_series else{})

    response = {"timeSeriesResponse": timeseries_response}

    return json.dumps(response)
