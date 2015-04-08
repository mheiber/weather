

from geopy.distance import great_circle as get_distance
from csv_to_json import *

lat_lons=csv_to_list_of_dicts('./zipLatLonNormalized.csv')
wbans=csv_to_list_of_dicts('./LU_WBAN.csv')

wbans_from_fact=csv_to_list_of_dicts('./LU_WBAN.csv')

distinct_wbans=reduce(lambda distinct_list,wban: distinct_list+[wban['WBAN']] if wban['WBAN'] not in distinct_list else distinct_list, wbans_from_fact,[])

wbans=filter(lambda wban: wban['WBAN'] in distinct_wbans,wbans)

out_dicts=[]

def location(dictionary):
	return (dictionary['lat'],dictionary['lon'])

def distance_between(dictionary1,dictionary2):
	location1=location(dictionary1)
	location2=location(dictionary2)
	return get_distance(location1,location2)

for lat_lon in lat_lons:
	lat_lon['closest_wban']=wbans[0]
	least_distance=distance_between(lat_lon,wbans[0])
	for wban in wbans:
		wban_distance=distance_between(lat_lon,wban)
		if wban_distance<least_distance:
			least_distance=wban_distance
			lat_lon['closest_wban']=int(wban['WBAN'])
	print lat_lon['zip'],'closests is',lat_lon['closest_wban']
list_of_dicts_to_csv(lat_lons,'closer2.csv')





