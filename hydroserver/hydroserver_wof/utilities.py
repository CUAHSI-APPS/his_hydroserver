from hydroserver_core.rest_api.models import Database
import time
import pandas as pd

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
        params.format = "waterml"

    database_details = Database.objects.get(collection_id=network, database_id=database)
    database_model = getattr(database_details, "database_type")
    database_path = getattr(database_details, "database_path")

    start = time.time()
    output_data = databases[database_model](network=network, database=database, database_path=database_path, params=params)
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
        tables[key] = tables[key].where((pd.notnull(tables[key])), None)
    return tables
