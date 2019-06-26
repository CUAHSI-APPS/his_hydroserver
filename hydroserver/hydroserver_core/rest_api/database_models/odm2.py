import sqlite3


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
