from hydroserver_core.rest_api.models import Database
import time
import pandas as pd


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


def get_content_type(response_format):

    content_type_list = {
        "waterml": "text/xml",
        "waterjson": "application/json"
    }

    content_type = content_type_list.get(response_format)

    if response_format is None:
        content_type = "text/xml"

    return content_type


def get_wof_response(databases, outputs, params):

    network = params.get("network")
    database = params.get("database")
    response_format = params.get("format")

    if response_format not in ["waterml", "waterjson"]:
        response_format = "waterml"
        params["format"] = "waterml"

    try:
        database_details = Database.objects.get(network_id=network, database_id=database)
    except Database.DoesNotExist:
        return "404_Not_Found"

    database_model = getattr(database_details, "database_type")
    database_path = getattr(database_details, "database_path")

    start = time.time()
    output_data = databases[database_model](network=network, database=database, database_path=database_path, params=params)
    if output_data == "400_Bad_Request":
        return "400_Bad_Request"
    print(f"Extraction Time: {time.time()-start} seconds")

    start = time.time()
    transformed_data = transform_tables(tables=output_data)
    print(f"Transformation Time: {time.time()-start} seconds")

    start = time.time()
    response = outputs[response_format](output_data=transformed_data)
    print(f"Loading Time: {time.time()-start} seconds")

    return response


def transform_tables(tables):
    for key in tables:
        if tables[key].empty:
            tables[key] = None
        else:
            tables[key] = tables[key].where((pd.notnull(tables[key])), None)
    return tables
