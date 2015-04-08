from csv_to_json import *
from collections import OrderedDict

fact_rows=csv_to_list_of_dicts('./201503daily.csv')
zip_codes=csv_to_list_of_dicts('./closer2.csv')


out_rows=[]

for fact_row in fact_rows:
	out_row=OrderedDict()
	print fact_row
	for zip_code in zip_codes:
		if zip_code['closest_wban']==fact_row['WBAN']:
			for key in fact_row.keys():
				out_row[key]=fact_row[key]
			out_row['zip']=zip_code['zip']
			print out_row,'\n\n'
			out_rows.append(out_row)


# for zip_code in zip_codes:
# 	out_row=OrderedDict()
# 	out_row['zip']=zip_code['zip']
# 	for fact_row in fact_rows:
# 		if fact_row['WBAN']==zip_code['closest_wban']:
# 			for key in fact_row.keys():
# 				out_row[key]=fact_row[key]
# 			out_rows.append(out_row)
# 			break

list_of_dicts_to_csv(out_rows,'facts3.csv')
print 'done'
