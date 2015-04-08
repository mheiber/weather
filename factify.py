from csv_to_json import *
from collections import OrderedDict



def factify(fact_file,closest_wbans_file,out_file):

	fact_rows=csv_to_list_of_dicts(fact_file)
	zip_codes=csv_to_list_of_dicts(closest_wbans_file)

	out_rows=[]
	length=len(fact_rows)

	for row_num,fact_row in enumerate(fact_rows):

		for zip_code in zip_codes:
			if zip_code['closest_wban_id']==fact_row['WBAN']:
				out_row=OrderedDict()
				out_row['zip']=zip_code['zip']
				for key in fact_row.keys():
					out_row[key]=fact_row[key]
				out_rows.append(out_row)
		print row_num,row_num*1.0/length

	list_of_dicts_to_csv(out_rows,out_file)
	print 'wrote to '+out_file