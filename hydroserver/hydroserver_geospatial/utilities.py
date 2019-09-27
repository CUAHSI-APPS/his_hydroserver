import requests
import json
import shapefile
import os
import shutil
from hydroserver import settings


def create_workspace(request_data):

    geoserver_url = settings.GEOSERVER_URL
    geoserver_user = settings.GEOSERVER_USER
    geoserver_pass = settings.GEOSERVER_PASS
    geoserver_auth = requests.auth.HTTPBasicAuth(
        geoserver_user, 
        geoserver_pass
    )

    workspace_id = f"TS-{request_data['network_id']}"

    headers = {
        "content-type": "application/json"
    }

    data = json.dumps({"workspace": {"name": workspace_id}})
    rest_url = f"{geoserver_url}/rest/workspaces"
    response = requests.post(rest_url, headers=headers, data=data, auth=geoserver_auth)

    try:
        os.mkdir(settings.HYDROSERVER_VAULT + request_data['network_id'])
    except:
        pass


def delete_workspace(network_id):

    geoserver_url = settings.GEOSERVER_URL
    geoserver_user = settings.GEOSERVER_USER
    geoserver_pass = settings.GEOSERVER_PASS
    geoserver_auth = requests.auth.HTTPBasicAuth(
        geoserver_user, 
        geoserver_pass
    )

    workspace_id = f"TS-{network_id}"

    headers = {
        "content-type": "application/json"
    }

    params = {
        "update": "overwrite", "recurse": True
    }

    rest_url = f"{geoserver_url}/rest/workspaces/{workspace_id}"
    response = requests.delete(rest_url, params=params, auth=geoserver_auth, headers=headers)

    try:
        shutil.rmtree(settings.HYDROSERVER_VAULT + network_id)
    except:
        pass


def create_datastore(reference_data, many):
    
    if not many:
        reference_data = [reference_data]
    w = shapefile.Writer(settings.HYDROSERVER_VAULT + reference_data[0]["network_id"] + "/" + reference_data[0]["database_id"])
    w.field("Site_Name", "C")
    w.field("Site_Code", "C")
    w.field("Variable_Name", "C")
    w.field("Variable_Code", "C")
    w.field("Sample_Medium", "C")
    w.field("Value_Count", "N")
    w.field("Begin_Date", "C")
    w.field("End_Date", "C")
    w.field("Method_Link", "C")
    w.field("Method_Description", "C")
    w.field("Network_ID", "C")
    w.field("Database_ID", "C")
    for ref in reference_data:
        w.point(ref["latitude"], ref["longitude"])
        w.record(
            ref["site_name"],
            ref["site_code"],
            ref["variable_name"],
            ref["variable_code"],
            ref["sample_medium"],
            ref["value_count"],
            ref["begin_date"],
            ref["end_date"],
            ref["method_link"],
            ref["method_description"],
            ref["network_id"],
            ref["database_id"]
        )
    w.close()
    shutil.copy(f"{os.path.dirname(os.path.realpath(__file__))}/template.prj", f"{settings.HYDROSERVER_VAULT}{reference_data[0]['network_id']}/{reference_data[0]['database_id']}.prj")

    geoserver_url = settings.GEOSERVER_URL
    geoserver_user = settings.GEOSERVER_USER
    geoserver_pass = settings.GEOSERVER_PASS
    geoserver_directory = settings.GEOSERVER_VAULT
    geoserver_auth = requests.auth.HTTPBasicAuth(
        geoserver_user, 
        geoserver_pass
    )

    workspace_id = f"TS-{reference_data[0]['network_id']}"

    headers = {
        "content-type": "application/json"
    }

    if any(i in reference_data[0]["database_id"] for i in [".", ","]):
        print("1")
        return False

    rest_url = f"{geoserver_url}/rest/workspaces/{workspace_id}/datastores/{reference_data[0]['database_id'].replace('/', ' ')}/external.shp"
    data = f"file://{geoserver_directory}/{reference_data[0]['network_id']}/{reference_data[0]['database_id']}.shp"
    response = requests.put(rest_url, data=data, headers=headers, auth=geoserver_auth)

    if response.status_code != 201:
        print("2")
        return False

    rest_url = f"{geoserver_url}/rest/workspaces/{workspace_id}/datastores/{reference_data[0]['database_id'].replace('/', ' ')}/featuretypes/{reference_data[0]['database_id']}.json"
    response = requests.get(rest_url, headers=headers, auth=geoserver_auth)

    try:
        if json.loads(response.content.decode('utf-8'))["featureType"]["enabled"] is False:
            print("3")
            return False
    except:
        print("4")
        return False

    data = response.content.decode('utf-8').replace('"name":"' + reference_data[0]["database_id"] + '"', '"name":"' + reference_data[0]["database_id"].replace("/", " ") + '"')
    response = requests.put(rest_url, headers=headers, auth=geoserver_auth, data=data)

    if response.status_code != 200:
        print("5")
        return False


def delete_datastore(network_id, database_id):

    geoserver_url = settings.GEOSERVER_URL
    geoserver_user = settings.GEOSERVER_USER
    geoserver_pass = settings.GEOSERVER_PASS
    geoserver_directory = settings.GEOSERVER_VAULT
    geoserver_auth = requests.auth.HTTPBasicAuth(
        geoserver_user, 
        geoserver_pass
    )

    workspace_id = f"TS-{network_id}"

    headers = {
        "content-type": "application/json"
    }

    params = {
        "update": "overwrite", "recurse": True
    }

    rest_url = f"{geoserver_url}/rest/workspaces/{workspace_id}/datastores/{database_id.replace('/', ' ')}"
    response = requests.delete(rest_url, params=params, headers=headers, auth=geoserver_auth)

    os.remove(f'{settings.HYDROSERVER_VAULT}{network_id}/{database_id}.shp')
    os.remove(f'{settings.HYDROSERVER_VAULT}{network_id}/{database_id}.prj')
    os.remove(f'{settings.HYDROSERVER_VAULT}{network_id}/{database_id}.dbf')
    os.remove(f'{settings.HYDROSERVER_VAULT}{network_id}/{database_id}.shx')
