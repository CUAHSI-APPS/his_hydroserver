from hydroserver_core.rest_api.models import Database


def build_refts(databases, params):

    network = params.get("network")
    database = params.get("database")
    query_url = params.get("query_url")

    try:
        database_details = Database.objects.get(network_id=network, database_id=database)
    except Database.DoesNotExist:
        return "404_Not_Found"

    database_model = getattr(database_details, "database_type")
    database_path = getattr(database_details, "database_path")

    refts_data = databases[database_model](network=network, database=database, database_path=database_path, params=params)

    if refts_data == "400_Bad_Request":
        return "400_Bad_Request"

    refts_metadata = refts_data.get("refts_metadata")
    refts_data_list = refts_data.get("refts_list")

    keywords = list(set([j for k in [[i[0], i[2], i[6], i[7]] for i in refts_data_list] for j in k]))

    refts_list = [
        {
            "beginDate": i[10],
            "endDate": i[11],
            "sampleMedium": i[0],
            "valueCount": i[1],
            "site": {
                "siteName": i[2],
                "siteCode": i[3],
                "latitude": i[4],
                "longitude": i[5]
            },
            "variable": {
                "variableName": i[6],
                "variableCode": i[7]
            },
            "method": {
                "methodLink": i[8],
                "methodDescription": i[9]
            },
            "requestInfo": {
                "refType": "WOF",
                "serviceType": "REST",
                "url": "/".join(query_url.split("/")[:-1]),
                "returnType": "WaterML 1.1",
                "network_name": network
            }

        } for i in refts_data_list
    ]

    refts = {
        "timeSeriesReferenceFile": {
            "fileVersion": "1.0.0",
            "title": refts_metadata[0][0],
            "abstract": refts_metadata[0][1],
            "keywords": keywords,
            "symbol": "https://www.hydroshare.org/static/img/logo-lg.png",
            "referencedTimeSeries": refts_list
        }
    }

    return refts


def build_geojson(databases, params):

    network = params.get("network")
    database = params.get("database")
    query_url = params.get("query_url")

    try:
        database_details = Database.objects.get(network_id=network, database_id=database)
    except Database.DoesNotExist:
        return "404_Not_Found"

    database_model = getattr(database_details, "database_type")
    database_path = getattr(database_details, "database_path")

    refts_data = databases[database_model](network=network, database=database, database_path=database_path, params=params)

    if refts_data == "400_Bad_Request":
        return "400_Bad_Request"

    refts_metadata = refts_data.get("refts_metadata")
    refts_data_list = refts_data.get("refts_list")

    feature_list = [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    i[5],
                    i[4],
                ]
            },
            "properties": {
                "Site Name": i[2],
                "Site Code": i[3],
                "Variable Name": i[6],
                "Variable Code": i[7],
                "Begin Date": i[10],
                "End Date": i[11],
                "Sample Medium": i[0],
                "Value Count": i[1],
                "Request URL": "/".join(query_url.split("/")[:-1]),
                "Network Name": network,
                "Method Link": i[8],
                "Method Description": i[9]
            }
        } for i in refts_data_list
    ]

    geojson = {
        "type": "FeatureCollection",
        "features": feature_list
    }

    return geojson
