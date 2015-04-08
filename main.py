from write_closest import write_closest
from factify import factify
from clean_results import clean_results
from csv_to_json import *


fact_file='201502daily.csv'
zip_codes_file='./zipLatLonNormalized.csv'
wbans_file='./LU_WBAN.csv'

dirty_results_file='results_results_201502.csv'
clean_results_file='results_clean_201502.csv'

closest_wbans_file='closest_201502.csv'

fact_rows=csv_to_list_of_dicts(fact_file)
zip_codes=csv_to_list_of_dicts(zip_codes_file)

config={}
with open('config.json','r') as f:
	config=json.load(f)

required_fields=config['required_fields']

#fact_file is CSV of format WBAN, facts ...
#wbans file is CSV of format WBAN, lat, lon
#output is closest_wbans_file of format zip,lat_lon,closest_wban_id
write_closest(fact_file,required_fields,zip_codes_file,wbans_file,closest_wbans_file)

# dirty_results_file is of format YearMonthDay,zip_code, facts
#inconsistent indication of null values, though: sometimes 'M', sometimes blank
factify(fact_file,closest_wbans_file,dirty_results_file)

#cleaned output has None values for nulls
clean_results(dirty_results_file,clean_results_file)

