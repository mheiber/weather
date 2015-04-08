
import json
from csv_to_json import *

from geopy.distance import great_circle as get_distance

def write_closest(fact_file,required_fields,zip_codes_file,wbans_file,out_file):

	def get_distinct_wbans():
		lat_lons=csv_to_list_of_dicts(zip_codes_file)
		wbans=csv_to_list_of_dicts(wbans_file)

		wbans_from_fact=csv_to_list_of_dicts(wbans_file)
		distinct_wbans=reduce(lambda distinct_list,wban: distinct_list+[wban['WBAN']] if wban['WBAN'] not in distinct_list else distinct_list, wbans_from_fact,[])
		wbans=filter(lambda wban: wban['WBAN'] in distinct_wbans,wbans)
		return wbans

	def location(dictionary):
		return (dictionary['lat'],dictionary['lon'])

	def distance_between(dictionary1,dictionary2):
		location1=location(dictionary1)
		location2=location(dictionary2)
		return get_distance(location1,location2)

	def closest_wban_id(lat_lon,wbans):
		lat_lon['closest_wban']=wbans[0]
		least_distance=distance_between(lat_lon,wbans[0])
		wban_id=wbans[0]['WBAN']
		for wban in wbans:
			wban_distance=distance_between(lat_lon,wban)
			if wban_distance<least_distance:
				least_distance=wban_distance
				wban_id=int(wban['WBAN'])
		print 'closest is',wban_id
		return wban_id


	def is_empty(value):
		return value in [None,'','M','m',' ','  ','\t']

	def is_valid_row(row):
		for field in required_fields:
			if is_empty(row[field]):
				return False
		return True


	def valid_wban_id_reducer(valids,fact_row):
		return valids+[fact_row['WBAN']] if fact_row['WBAN'] not in valids else valids


	fact_rows=csv_to_list_of_dicts(fact_file)
	valid_fact_rows=filter(is_valid_row,fact_rows)
	print 'valid fact rows',len(valid_fact_rows)
	valid_wban_ids=reduce(valid_wban_id_reducer,valid_fact_rows,[])
	print 'valids length',len(valid_wban_ids)
	#closes over three vars above
	def is_valid_wban(wban):
		return wban['WBAN'] in valid_wban_ids

	distinct_wbans=get_distinct_wbans()
	print 'distinct', len(distinct_wbans)
	wbans=filter(is_valid_wban,distinct_wbans)	#We now have a list of WBANs that have values for all

	#required fields for the whole month

	print 'got list of valid wbans',len(wbans)
	zip_codes=csv_to_list_of_dicts(zip_codes_file)
	for zip_code in zip_codes:
		zip_code['closest_wban_id']=closest_wban_id(zip_code,wbans)

	list_of_dicts_to_csv(zip_codes,out_file)











