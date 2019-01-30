import pandas as pd
import sqlite3
import datetime
from hydroserver_wof.models import WofModels


def get_sites(network, database, database_path, params):

    try:
        sql_connect = sqlite3.connect(database_path, isolation_level=None)
    except:
        return "400_Bad_Request"

    cursor = sql_connect.cursor()

    query_table = WofModels.query_table
    site_info_table = WofModels.site_info_table

    creation_time = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00"))
    query_url = params["query_url"].replace("&", "&amp;")
    method_called = "GetSites"
    location_param = None
    variable_param = None
    begin_datetime = None
    end_datetime = None

    query_data = [(
        creation_time, 
        query_url, 
        method_called,
        location_param, 
        variable_param, 
        begin_datetime,
        end_datetime
    )]

    query_table = query_table.append(pd.DataFrame(query_data, columns=query_table.columns))

    cursor.execute(f"""SELECT SamplingFeatures.SamplingFeatureCode, 
                              SamplingFeatures.SamplingFeatureName, 
                              Sites.Latitude, 
                              Sites.Longitude,
                              SamplingFeatures.Elevation_m,
                              SamplingFeatures.ElevationDatumCV

                       FROM SamplingFeatures 
                       INNER JOIN Sites
                       ON SamplingFeatures.SamplingFeatureID = Sites.SamplingFeatureID""")

    site_info_table = site_info_table.append(pd.DataFrame(cursor.fetchall(), columns=site_info_table.columns))

    sites_data = {
        "query_table": query_table,
        "site_info_table": site_info_table
    }

    return sites_data


def get_site_info(network, database, database_path, params):

    try:
        sql_connect = sqlite3.connect(database_path, isolation_level=None)
    except:
        return "400_Bad_Request"

    cursor = sql_connect.cursor()

    query_table = WofModels.query_table
    site_info_table = WofModels.site_info_table
    series_catalog_table = WofModels.series_catalog_table
    variable_info_table = WofModels.variable_info_table
    method_table = WofModels.method_table
    source_table = WofModels.source_table

    creation_time = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00"))
    query_url = params["query_url"].replace("&", "&amp;")
    method_called = "GetSiteInfo"
    location_param = params["site_code"]
    variable_param = None
    begin_datetime = None
    end_datetime = None

    query_data = [(
        creation_time, 
        query_url, 
        method_called,
        location_param, 
        variable_param, 
        begin_datetime,
        end_datetime
    )]

    query_table = query_table.append(pd.DataFrame(query_data, columns=query_table.columns))

    cursor.execute(f"""SELECT SamplingFeatures.SamplingFeatureCode, 
                              SamplingFeatures.SamplingFeatureName, 
                              Sites.Latitude, 
                              Sites.Longitude,
                              SamplingFeatures.Elevation_m,
                              SamplingFeatures.ElevationDatumCV

                       FROM SamplingFeatures 
                       INNER JOIN Sites
                       ON SamplingFeatures.SamplingFeatureID = Sites.SamplingFeatureID
                       WHERE SamplingFeatures.SamplingFeatureCode = '{str(location_param)}'""")

    site_info_table = site_info_table.append(pd.DataFrame(cursor.fetchall(), columns=site_info_table.columns))

    cursor.execute(f"""SELECT Results.ValueCount,
                              Actions.BeginDateTime,
                              Actions.EndDateTime

                       FROM Results
                       INNER JOIN FeatureActions
                       ON Results.FeatureActionID = FeatureActions.FeatureActionID
                       INNER JOIN Actions
                       ON FeatureActions.ActionID = Actions.ActionID
                       INNER JOIN SamplingFeatures
                       ON FeatureActions.SamplingFeatureID = SamplingFeatures.SamplingFeatureID
                       WHERE SamplingFeatures.SamplingFeatureCode = '{str(location_param)}'""")

    series_catalog_table = series_catalog_table.append(pd.DataFrame(cursor.fetchall(), columns=series_catalog_table.columns))

    cursor.execute(f"""SELECT Methods.MethodCode,
                              Methods.MethodDescription,
                              Methods.MethodLink

                       FROM Results
                       INNER JOIN FeatureActions
                       ON Results.FeatureActionID = FeatureActions.FeatureActionID
                       INNER JOIN Actions
                       ON FeatureActions.ActionID = Actions.ActionID
                       INNER JOIN Methods
                       ON Actions.MethodID = Methods.MethodID
                       INNER JOIN SamplingFeatures
                       ON FeatureActions.SamplingFeatureID = SamplingFeatures.SamplingFeatureID
                       WHERE SamplingFeatures.SamplingFeatureCode = '{str(location_param)}'""")

    method_table = method_table.append(pd.DataFrame(cursor.fetchall(), columns=method_table.columns))

    cursor.execute(f"""SELECT Organizations.OrganizationCode,
                              Organizations.OrganizationName,
                              Organizations.OrganizationDescription,
                              People.PersonFirstName || People.PersonLastName,
                              ActionBy.RoleDescription,
                              Affiliations.PrimaryPhone,
                              Affiliations.PrimaryEmail,
                              Affiliations.PrimaryAddress,
                              Organizations.OrganizationLink

                       FROM Results
                       INNER JOIN FeatureActions
                       ON Results.FeatureActionID = FeatureActions.FeatureActionID
                       INNER JOIN Actions
                       ON FeatureActions.ActionID = Actions.ActionID
                       INNER JOIN ActionBy
                       ON Actions.ActionID = ActionBy.ActionID
                       INNER JOIN Affiliations
                       ON ActionBy.AffiliationID = Affiliations.AffiliationID
                       INNER JOIN Organizations
                       ON Affiliations.OrganizationID = Organizations.OrganizationID
                       INNER JOIN People
                       ON Affiliations.PersonID = People.PersonID
                       INNER JOIN SamplingFeatures
                       ON FeatureActions.SamplingFeatureID = SamplingFeatures.SamplingFeatureID
                       WHERE SamplingFeatures.SamplingFeatureCode = '{str(location_param)}'""")

    source_table = source_table.append(pd.DataFrame(cursor.fetchall(), columns=source_table.columns))

    cursor.execute(f"""SELECT Variables.VariableCode,
                              Variables.VariableNameCV,
                              Variables.VariableDefinition,
                              Units.UnitsName,
                              Units.UnitsAbbreviation,
                              Units.UnitsID,
                              Variables.NoDataValue

                       FROM Results
                       INNER JOIN Units
                       ON Results.UnitsID = Units.UnitsID
                       INNER JOIN Variables
                       ON Results.VariableID = Variables.VariableID
                       INNER JOIN FeatureActions
                       ON Results.FeatureActionID = FeatureActions.FeatureActionID
                       INNER JOIN SamplingFeatures
                       ON FeatureActions.SamplingFeatureID = SamplingFeatures.SamplingFeatureID
                       WHERE SamplingFeatures.SamplingFeatureCode = '{str(location_param)}'""")

    variable_info_table = variable_info_table.append(pd.DataFrame(cursor.fetchall(), columns=variable_info_table.columns))

    site_info_data = {
        "query_table": query_table,
        "site_info_table": site_info_table,
        "series_catalog_table": series_catalog_table,
        "method_table": method_table,
        "source_table": source_table,
        "variable_info_table": variable_info_table
    }

    return site_info_data


def get_variables(network, database, database_path, params):

    try:
        sql_connect = sqlite3.connect(database_path, isolation_level=None)
    except:
        return "400_Bad_Request"

    cursor = sql_connect.cursor()

    query_table = WofModels.query_table
    variable_info_table = WofModels.variable_info_table

    creation_time = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00"))
    query_url = params["query_url"].replace("&", "&amp;")
    method_called = "GetVariables"
    location_param = None
    variable_param = None
    begin_datetime = None
    end_datetime = None

    query_data = [(
        creation_time, 
        query_url, 
        method_called,
        location_param, 
        variable_param, 
        begin_datetime,
        end_datetime
    )]

    query_table = query_table.append(pd.DataFrame(query_data, columns=query_table.columns))

    cursor.execute(f"""SELECT Variables.VariableCode,
                              Variables.VariableNameCV,
                              Variables.VariableDefinition,
                              Units.UnitsName,
                              Units.UnitsAbbreviation,
                              Units.UnitsID,
                              Variables.NoDataValue

                       FROM Results
                       INNER JOIN Units
                       ON Results.UnitsID = Units.UnitsID
                       INNER JOIN Variables
                       ON Results.VariableID = Variables.VariableID
                       WHERE Results.ResultID IN
                       (SELECT MIN(Results.ResultID) 
                        FROM Results
                        GROUP BY VariableID, UnitsID)""")

    variable_info_table = variable_info_table.append(pd.DataFrame(cursor.fetchall(), columns=variable_info_table.columns))

    variables_data = {
        "query_table": query_table,
        "variable_info_table": variable_info_table
    }

    return variables_data


def get_variable_info(network, database, database_path, params):

    try:
        sql_connect = sqlite3.connect(database_path, isolation_level=None)
    except:
        return "400_Bad_Request"

    cursor = sql_connect.cursor()

    query_table = WofModels.query_table
    variable_info_table = WofModels.variable_info_table

    creation_time = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00"))
    query_url = params["query_url"].replace("&", "&amp;")
    method_called = "GetVariableInfo"
    location_param = None
    variable_param = params["variable_code"]
    begin_datetime = None
    end_datetime = None

    query_data = [(
        creation_time, 
        query_url, 
        method_called,
        location_param, 
        variable_param, 
        begin_datetime,
        end_datetime
    )]

    query_table = query_table.append(pd.DataFrame(query_data, columns=query_table.columns))

    cursor.execute(f"""SELECT Variables.VariableCode,
                              Variables.VariableNameCV,
                              Variables.VariableDefinition,
                              Units.UnitsName,
                              Units.UnitsAbbreviation,
                              Units.UnitsID,
                              Variables.NoDataValue

                       FROM Results
                       INNER JOIN Units
                       ON Results.UnitsID = Units.UnitsID
                       INNER JOIN Variables
                       ON Results.VariableID = Variables.VariableID
                       WHERE Variables.VariableCode = '{str(variable_param)}'
                       GROUP BY Results.VariableID""")

    variable_info_table = variable_info_table.append(pd.DataFrame(cursor.fetchall(), columns=variable_info_table.columns))

    variables_data = {
        "query_table": query_table,
        "variable_info_table": variable_info_table
    }

    return variables_data


def get_values(network, database, database_path, params):

    try:
        sql_connect = sqlite3.connect(database_path, isolation_level=None)
    except:
        return "400_Bad_Request"

    cursor = sql_connect.cursor()

    query_table = WofModels.query_table
    site_info_table = WofModels.site_info_table
    values_table = WofModels.values_table
    variable_info_table = WofModels.variable_info_table
    method_table = WofModels.method_table
    source_table = WofModels.source_table

    creation_time = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00"))
    query_url = params["query_url"].replace("&", "&amp;")
    method_called = "GetValues"
    location_param = params["site_code"]
    variable_param = params["variable_code"]
    begin_datetime = params["start_time"]
    end_datetime = params["end_time"]

    query_data = [(
        creation_time, 
        query_url, 
        method_called,
        location_param, 
        variable_param, 
        begin_datetime,
        end_datetime
    )]

    query_table = query_table.append(pd.DataFrame(query_data, columns=query_table.columns))

    cursor.execute(f"""SELECT SamplingFeatures.SamplingFeatureCode, 
                              SamplingFeatures.SamplingFeatureName, 
                              Sites.Latitude, 
                              Sites.Longitude,
                              SamplingFeatures.Elevation_m,
                              SamplingFeatures.ElevationDatumCV

                       FROM SamplingFeatures 
                       INNER JOIN Sites
                       ON SamplingFeatures.SamplingFeatureID = Sites.SamplingFeatureID
                       WHERE SamplingFeatures.SamplingFeatureCode = '{str(location_param)}'""")

    site_info_table = site_info_table.append(pd.DataFrame(cursor.fetchall(), columns=site_info_table.columns))

    cursor.execute(f"""SELECT Variables.VariableCode,
                              Variables.VariableNameCV,
                              Variables.VariableDefinition,
                              Units.UnitsName,
                              Units.UnitsAbbreviation,
                              Units.UnitsID,
                              Variables.NoDataValue

                       FROM Results
                       INNER JOIN Units
                       ON Results.UnitsID = Units.UnitsID
                       INNER JOIN Variables
                       ON Results.VariableID = Variables.VariableID
                       WHERE Variables.VariableCode = '{str(variable_param)}'
                       GROUP BY Results.VariableID""")

    variable_info_table = variable_info_table.append(pd.DataFrame(cursor.fetchall(), columns=variable_info_table.columns))

    cursor.execute(f"""SELECT Methods.MethodCode AS MethodCode,
                              Methods.MethodDescription,
                              Methods.MethodLink

                       FROM Results
                       INNER JOIN FeatureActions
                       ON Results.FeatureActionID = FeatureActions.FeatureActionID
                       INNER JOIN Actions
                       ON FeatureActions.ActionID = Actions.ActionID
                       INNER JOIN Methods
                       ON Actions.MethodID = Methods.MethodID
                       INNER JOIN Variables
                       ON Results.VariableID = Variables.VariableID
                       INNER JOIN SamplingFeatures
                       ON FeatureActions.SamplingFeatureID = SamplingFeatures.SamplingFeatureID
                       WHERE SamplingFeatures.SamplingFeatureCode = '{str(location_param)}'
                       AND Variables.VariableCode = '{str(variable_param)}'
                       GROUP BY MethodCode""")

    method_table = method_table.append(pd.DataFrame(cursor.fetchall(), columns=method_table.columns))

    cursor.execute(f"""SELECT Organizations.OrganizationCode AS OrganizationCode,
                              Organizations.OrganizationName,
                              Organizations.OrganizationDescription,
                              People.PersonFirstName || People.PersonLastName,
                              ActionBy.RoleDescription,
                              Affiliations.PrimaryPhone,
                              Affiliations.PrimaryEmail,
                              Affiliations.PrimaryAddress,
                              Organizations.OrganizationLink

                       FROM Results
                       INNER JOIN FeatureActions
                       ON Results.FeatureActionID = FeatureActions.FeatureActionID
                       INNER JOIN Actions
                       ON FeatureActions.ActionID = Actions.ActionID
                       INNER JOIN ActionBy
                       ON Actions.ActionID = ActionBy.ActionID
                       INNER JOIN Affiliations
                       ON ActionBy.AffiliationID = Affiliations.AffiliationID
                       INNER JOIN Organizations
                       ON Affiliations.OrganizationID = Organizations.OrganizationID
                       INNER JOIN People
                       ON Affiliations.PersonID = People.PersonID
                       INNER JOIN Variables
                       ON Results.VariableID = Variables.VariableID
                       INNER JOIN SamplingFeatures
                       ON FeatureActions.SamplingFeatureID = SamplingFeatures.SamplingFeatureID
                       WHERE SamplingFeatures.SamplingFeatureCode = '{str(location_param)}'
                       AND Variables.VariableCode = '{str(variable_param)}'
                       GROUP BY OrganizationCode""")

    source_table = source_table.append(pd.DataFrame(cursor.fetchall(), columns=source_table.columns))

    cursor.execute(f"""SELECT TimeSeriesResultValues.DataValue,
                              TimeSeriesResultValues.ValueDateTime,
                              TimeSeriesResultValues.ValueDateTimeUTCOffset,
                              Methods.MethodCode,
                              Organizations.OrganizationCode

                       FROM TimeSeriesResultValues
                       INNER JOIN Results
                       ON TimeSeriesResultValues.ResultID = Results.ResultID
                       INNER JOIN FeatureActions
                       ON Results.FeatureActionID = FeatureActions.FeatureActionID
                       INNER JOIN Actions
                       ON FeatureActions.ActionID = Actions.ActionID
                       INNER JOIN ActionBy
                       ON ActionBy.ActionID = Actions.ActionID
                       INNER JOIN Affiliations
                       ON ActionBy.AffiliationID = Affiliations.AffiliationID 
                       INNER JOIN Methods
                       ON Actions.MethodID = Methods.MethodID
                       INNER JOIN Organizations
                       ON Affiliations.OrganizationID = Organizations.OrganizationID
                       INNER JOIN Variables
                       ON Results.VariableID = Variables.VariableID
                       INNER JOIN SamplingFeatures
                       ON FeatureActions.SamplingFeatureID = SamplingFeatures.SamplingFeatureID
                       WHERE Variables.VariableCode = '{str(variable_param)}'
                       AND SamplingFeatures.SamplingFeatureCode = '{str(location_param)}'
                       {f"AND datetime(TimeSeriesResultValues.ValueDateTime) > datetime('{str(begin_datetime)}')" if begin_datetime else ""}
                       {f"AND datetime(TimeSeriesResultValues.ValueDateTime) < datetime('{str(end_datetime)}')" if end_datetime else ""}""")

    values_table = values_table.append(pd.DataFrame(cursor.fetchall(), columns=values_table.columns))

    values_data = {
        "query_table": query_table,
        "variable_info_table": variable_info_table,
        "site_info_table": site_info_table,
        "method_table": method_table,
        "source_table": source_table,
        "values_table": values_table
    }

    return values_data
