from django.conf import settings
import json


def get_refts(output_data):

    ref_types = {
        "WOF": "wof"
    }

    response = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        i["longitude"],
                        i["latitude"]
                    ]
                },
                "properties": {
                    "siteName": i["site_name"],
                    "siteCode": i["site_code"],
                    "variableName": i["variable_name"],
                    "variableCode": i["variable_code"],
                    "beginDate": str(i["begin_date"]),
                    "endDate": str(i["end_date"]),
                    "sampleMedium": i["sample_medium"],
                    "valueCount": i["value_count"],
                    "methodLink": i["method_link"],
                    "methodDescription": i["method_description"],
                    "refType": output_data["ref_type"],
                    "serviceType": output_data["service_type"],
                    "url": f"{settings.PROXY_BASE_URL}/{ref_types[output_data['ref_type']]}/{i['network_id']}/{i['database_id']}/",
                    "returnType": output_data["return_type"],
                    "networkName": i["network_id"]
                }
            } for i in output_data["refts_data"]
        ]
    }

    return json.dumps(response)
