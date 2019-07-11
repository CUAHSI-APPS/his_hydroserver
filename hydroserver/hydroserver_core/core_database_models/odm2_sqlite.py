import pandas as pd
import sqlite3
from hydroserver_core.dao import CatalogModels


def get_catalog_info(network, database, database_path):
    
    try:
        sql_connect = sqlite3.connect(database_path, isolation_level=None)
    except:
        return "400_Bad_Request"

    cursor = sql_connect.cursor()

    catalog_table = CatalogModels.catalog_table

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

    catalog_table = catalog_table.append(pd.DataFrame(cursor.fetchall(), columns=catalog_table.columns))

    sql_connect.close()

    return catalog_table
