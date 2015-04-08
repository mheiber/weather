
import json
from csv_to_json import *
from utils import is_empty
from geopy.distance import great_circle as get_distance


def _get_distinct_wbans(wbans_from_fact):
	distinct_wban_ids=reduce(lambda distinct_list,wban: distinct_list+[wban['WBAN']] if wban['WBAN'] not in distinct_list else distinct_list, wbans_from_fact,[])
	wbans=filter(lambda wban: wban['WBAN'] in distinct_wban_ids,wbans_from_fact)
	return wbans

def _location(dictionary):
	return (dictionary['lat'],dictionary['lon'])

def _distance_between(dictionary1,dictionary2):
	location1=_location(dictionary1)
	location2=_location(dictionary2)
	return get_distance(location1,location2)

def _closest_wban_id(lat_lon,wbans):
	lat_lon['closest_wban']=wbans[0]
	least_distance=_distance_between(lat_lon,wbans[0])
	wban_id=wbans[0]['WBAN']
	for wban in wbans:
		wban_distance=_distance_between(lat_lon,wban)
		if wban_distance<least_distance:
			least_distance=wban_distance
			wban_id=int(wban['WBAN'])
	print 'closest is',wban_id
	return wban_id

def write_closest(fact_file,required_fields,zip_codes_file,wbans_file,out_file):

	#closes over required_fields
	def _is_valid_row(row):
		for field in required_fields:
			if is_empty(row[field]):
				return False
		return True

	fact_rows=csv_to_list_of_dicts(fact_file)
	valid_fact_rows=filter(_is_valid_row,fact_rows)
	wbans=csv_to_list_of_dicts(wbans_file)


	def _is_valid_wban(wban):
		for fact_row in fact_rows:
			if fact_row['WBAN']==wban['WBAN'] and not _is_valid_row(fact_row):
				print 'invalid wban',fact_row
				return False
		return True

	
	distinct_wbans=_get_distinct_wbans(wbans)
	print 'distinct', len(distinct_wbans)
	wbans=filter(_is_valid_wban,distinct_wbans)
	#We now have a list of WBANs that have values for all
	#required fields for the whole month

	print 'got list of valid wbans',len(wbans)
	zip_codes=csv_to_list_of_dicts(zip_codes_file)
	for zip_code in zip_codes:
		zip_code['closest_wban_id']=_closest_wban_id(zip_code,wbans)

	list_of_dicts_to_csv(zip_codes,out_file)










