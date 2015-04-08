from write_closest import write_closest
from factify import factify
from csv_to_json import *


fact_file='201503daily.csv'
zip_codes_file='./zipLatLonNormalized.csv'
wbans_file='./LU_WBAN.csv'

closest_wbans_file='closest_v3.csv'

fact_rows=csv_to_list_of_dicts(fact_file)
zip_codes=csv_to_list_of_dicts(zip_codes_file)

config={}
with open('config.json','r') as f:
	config=json.load(f)

required_fields=config['required_fields']



write_closest(fact_file,required_fields,zip_codes_file,wbans_file,closest_wbans_file)

factify(fact_file,closest_wbans_file,'results_results.csv')

