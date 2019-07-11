from hydroserver_core.models import Reference as ReferenceModel
import time


def get_response_info(content_type):

    if content_type == "application/refts+json":
        response_format = "reftsjson"
        response_type = "application/json"
    elif content_type == "application/geo+json":
        response_format = "reftsgeojson"
        response_type = "application/json"
    else:
        response_format = "reftsjson"
        response_type = "application/json"

    return response_format, response_type


def get_refts_response(outputs, params, response_format):

    parameters = {}

    if params["site_name"]:
        parameters["site_name__in"] = params["site_name"]
    if params["site_code"]:
        parameters["site_code__in"] = params["site_code"]
    if params["variable_name"]:
        parameters["variable_name__in"] = params["variable_name"]
    if params["variable_code"]:
        parameters["variable_code__in"] = params["variable_code"]
    if params["sample_medium"]:
        parameters["sample_medium__in"] = params["sample_medium"]
    if params["method_link"]:
        parameters["method_link__in"] = params["method_link"]
    if params["min_value_count"]:
        parameters["value_count__gte"] = params["min_value_count"]
    if params["max_value_count"]:
        parameters["value_count__lte"] = params["max_value_count"]
    if params["begin_date"]:
        parameters["begin_date__gte"] = params["begin_date"]
    if params["end_date"]:
        parameters["end_date__lte"] = params["end_date"]
    if params["north"]:
        parameters["latitude__lte"] = params["north"]
    if params["south"]:
        parameters["latitude__gte"] = params["south"]
    if params["east"]:
        parameters["longitude__lte"] = params["east"]
    if params["west"]:
        parameters["longitude__gte"] = params["west"]
    if params["network_id"]:
        parameters["network_id__in"] = params["network_id"]
    if params["database_id"]:
        parameters["database_id__in"] = params["database_id"]

    refts_data = list(ReferenceModel.objects.filter(**parameters).values())
    if not refts_data:
        return {}
    variable_list = [refts_data[0]["variable_name"].replace(",", "").lower()] + [i["variable_name"].replace(",", "").lower() for i in refts_data[1:]]
    variable_list = list(set(variable_list))
    variable_list[0] = variable_list[0].capitalize()
    if len(variable_list) == 1:
        variable_list = variable_list[0]
    if len(variable_list) == 2:
        variable_list = " and ".join(variable_list)
    if len(variable_list) > 2:
        variable_list = ", ".join(variable_list[:-1]) + " and " + variable_list[-1]
    site_list = [refts_data[0]["site_name"].replace(",", "")] + [i["site_name"].replace(",", "") for i in refts_data[1:]]
    site_list = list(set(site_list))
    if len(site_list) == 1:
        site_list = site_list[0]
    if len(site_list) == 2:
        site_list = " and ".join(site_list)
    if len(site_list) > 2:
        site_list = ", ".join(site_list[:-1]) + " and " + site_list[-1]
    start_date = min([i["begin_date"] for i in refts_data])
    end_date = max([i["end_date"] for i in refts_data])
    abstract = f"{variable_list} data collected from {start_date} to {end_date} from the following site{'s' if len(site_list) > 1 else ''}: {site_list}. Data hosted by the HydroShare Water Data Server."
    keywords = list(set([k for j in [[i["site_name"].replace(",", ""), i["variable_name"].replace(",", ""), i["sample_medium"].replace(",", "")] for i in refts_data] for k in j]))

    output_data = {
        "title": "Time series dataset hosted by the HydroShare Water Data Server",
        "abstract": abstract,
        "keywords": keywords,
        "service_type": params["service_type"] if params["service_type"] else "REST",
        "return_type": params["return_type"] if params["return_type"] else "WaterML 1.1",
        "ref_type": params["ref_type"] if params["ref_type"] else "WOF",
        "refts_data": refts_data
    }

    start = time.time()
    response = outputs[response_format](output_data=output_data)
    print(f"Loading Time: {time.time()-start} seconds")

    return response
