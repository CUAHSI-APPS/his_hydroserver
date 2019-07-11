from hydroserver_core.models import Database
import time
import pandas as pd


def get_response_info(content_type):

    if content_type == "application/wml+xml":
        response_format = "waterml"
        response_type = "application/xml"
    elif content_type == "application/water+json":
        response_format = "waterjson"
        response_type = "application/json"
    else:
        response_format = "waterml"
        response_type = "application/xml"

    return response_format, response_type


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
