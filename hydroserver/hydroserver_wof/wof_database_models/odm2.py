import pandas as pd
import sqlite3
import datetime
from hydroserver_wof.models import WofModels


def refts(network, database, database_path, params):
    
    try:
        sql_connect = sqlite3.connect(database_path, isolation_level=None)
    except:
        return "400_Bad_Request"

    cursor = sql_connect.cursor()

    cursor.execute(f"""SELECT Results.SampledMediumCV,
                              Results.ValueCount,
                              SamplingFeatures.SamplingFeatureName,
                              SamplingFeatures.SamplingFeatureCode,
                              Sites.Latitude,
                              Sites.Longitude,
                              Variables.VariableNameCV,
                              Variables.VariableCode,
                              Methods.MethodLink,
                              Methods.MethodDescription,
                              Actions.BeginDateTime,
                              Actions.EndDateTime

                       FROM Results
                       INNER JOIN FeatureActions
                       ON Results.FeatureActionID = FeatureActions.FeatureActionID
                       INNER JOIN Actions
                       ON FeatureActions.ActionID = Actions.ActionID
                       INNER JOIN Methods
                       ON Actions.MethodID = Methods.MethodID
                       INNER JOIN SamplingFeatures
                       ON FeatureActions.SamplingFeatureID = SamplingFeatures.SamplingFeatureID
                       INNER JOIN Sites
                       ON FeatureActions.SamplingFeatureID = Sites.SamplingFeatureID
                       INNER JOIN Variables
                       ON Results.VariableID = Variables.VariableID""")

    refts_list = cursor.fetchall()

    cursor.execute(f"""SELECT Datasets.DatasetTitle,
                              Datasets.DatasetAbstract

                       FROM Datasets""")

    refts_metadata = cursor.fetchall()

    refts_data = {
        "refts_list": refts_list,
        "refts_metadata": refts_metadata
    }

    sql_connect.close()

    return refts_data


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

    sql_connect.close()

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
                       WHERE SamplingFeatures.SamplingFeatureCode = ?""", (str(location_param),))

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
                       WHERE SamplingFeatures.SamplingFeatureCode = ?""", (str(location_param),))

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
                       WHERE SamplingFeatures.SamplingFeatureCode = ?""", (str(location_param),))

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
                       WHERE SamplingFeatures.SamplingFeatureCode = ?""", (str(location_param),))

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
                       WHERE SamplingFeatures.SamplingFeatureCode = ?""", (str(location_param),))

    variable_info_table = variable_info_table.append(pd.DataFrame(cursor.fetchall(), columns=variable_info_table.columns))

    site_info_data = {
        "query_table": query_table,
        "site_info_table": site_info_table,
        "series_catalog_table": series_catalog_table,
        "method_table": method_table,
        "source_table": source_table,
        "variable_info_table": variable_info_table
    }

    sql_connect.close()

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

    sql_connect.close()

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
                       WHERE Variables.VariableCode = ?
                       GROUP BY Results.VariableID""", (str(variable_param),))

    variable_info_table = variable_info_table.append(pd.DataFrame(cursor.fetchall(), columns=variable_info_table.columns))

    variables_data = {
        "query_table": query_table,
        "variable_info_table": variable_info_table
    }

    sql_connect.close()

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
                       WHERE SamplingFeatures.SamplingFeatureCode = ?""", (str(location_param),))

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
                       WHERE Variables.VariableCode = ?
                       GROUP BY Results.VariableID""", (str(variable_param),))

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
                       WHERE SamplingFeatures.SamplingFeatureCode = ? 
                       AND Variables.VariableCode = ?
                       GROUP BY MethodCode""", (str(location_param), str(variable_param),))

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
                       WHERE SamplingFeatures.SamplingFeatureCode = ? 
                       AND Variables.VariableCode = ?
                       GROUP BY OrganizationCode""", (str(location_param), str(variable_param),))

    source_table = source_table.append(pd.DataFrame(cursor.fetchall(), columns=source_table.columns))

    value_params = [variable_param, location_param]
    if begin_datetime:
        value_params.append(begin_datetime)
    if end_datetime:
        value_params.append(end_datetime)
    value_params = tuple(value_params)

    cursor.execute(f"""SELECT TimeSeriesResultValues.DataValue,
                              TimeSeriesResultValues.ValueDateTime,
                              TimeSeriesResultValues.ValueDateTimeUTCOffset,
                              Methods.MethodCode,
                              Organizations.OrganizationCode

                       FROM TimeSeriesResultValues
                       LEFT OUTER JOIN Results
                       ON TimeSeriesResultValues.ResultID = Results.ResultID
                       LEFT OUTER JOIN FeatureActions
                       ON Results.FeatureActionID = FeatureActions.FeatureActionID
                       LEFT OUTER JOIN Actions
                       ON FeatureActions.ActionID = Actions.ActionID
                       LEFT OUTER JOIN ActionBy
                       ON ActionBy.ActionID = Actions.ActionID
                       LEFT OUTER JOIN Affiliations
                       ON ActionBy.AffiliationID = Affiliations.AffiliationID 
                       LEFT OUTER JOIN Methods
                       ON Actions.MethodID = Methods.MethodID
                       LEFT OUTER JOIN Organizations
                       ON Affiliations.OrganizationID = Organizations.OrganizationID
                       LEFT OUTER JOIN Variables
                       ON Results.VariableID = Variables.VariableID
                       LEFT OUTER JOIN SamplingFeatures
                       ON FeatureActions.SamplingFeatureID = SamplingFeatures.SamplingFeatureID
                       WHERE Variables.VariableCode = ?
                       AND SamplingFeatures.SamplingFeatureCode = ?
                       {f"AND datetime(TimeSeriesResultValues.ValueDateTime) >= datetime(?)" if begin_datetime else ""}
                       {f"AND datetime(TimeSeriesResultValues.ValueDateTime) <= datetime(?)" if end_datetime else ""}""", value_params)

    values_table = values_table.append(pd.DataFrame(cursor.fetchall(), columns=values_table.columns))

    values_data = {
        "query_table": query_table,
        "variable_info_table": variable_info_table,
        "site_info_table": site_info_table,
        "method_table": method_table,
        "source_table": source_table,
        "values_table": values_table
    }

    sql_connect.close()

    return values_data
