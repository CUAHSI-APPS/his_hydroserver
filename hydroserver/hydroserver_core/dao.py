import pandas as pd


class CatalogModels():

	catalog_table = pd.DataFrame(columns = [
		"sample_medium",
		"value_count",
		"site_name",
		"site_code",
		"latitude",
		"longitude",
		"variable_name",
		"variable_code",
		"method_link",
		"method_description",
		"begin_date",
		"end_date"
	])
