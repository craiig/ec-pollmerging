#!/usr/bin/python

import sys, csv, re
import itertools #groupby
from pprint import pprint

if len(sys.argv) < 2:
	print "usage: combine_polls.py <csv_file>"
	sys.exit()

csvfile = open(sys.argv[1])
data = csv.DictReader(csvfile)

debug_combine = 0

#used as part of the key function as well as the combiner (all other columns get summed)
group_by_keys = [
 'Electoral District Name/Nom de circonscription',
 'Electoral District Number/Num\xe9ro de circonscription',
 'Polling Station Name/Nom du bureau de scrutin', 
 #'Polling Station Number/Num\xe9ro du bureau de scrutin', #polling station number is handled specially
]

polling_station_number = 'Polling Station Number/Num\xe9ro du bureau de scrutin'

merged_record_list_key = "Merged Poll Numbers"

sorted_by_polling_station = sorted(data, lambda x,y: cmp(x[polling_station_number], y[polling_station_number]) )

#function to help combine the split polls
def keyfunc(x):
	#strip off trailing A,B,.. from the station number
	orig = x[polling_station_number]
	rep = re.sub("[A-Za-z]*$", "", orig)

	key = ""
	for k in group_by_keys:
		key += x[k]
	key += " "+rep
	return key

new_records	 = []

for (k,v) in itertools.groupby(sorted_by_polling_station, key=keyfunc):
	count = 0
	combined_record = {}
	if debug_combine:
		print "-------"
	for r in v:
		count = count + 1

		if len(combined_record) == 0:
			if debug_combine:
				pprint(r)
			combined_record = r
			combined_record[merged_record_list_key] = str(combined_record[polling_station_number]) + " "
			combined_record[polling_station_number] = re.sub("[A-Za-z]*$", "", combined_record[polling_station_number])
		else:
			if debug_combine:
				print "+"
				pprint(r)

			#combine record, this is very hacky way to handle blank items as well as
			# the fact that "Merged with" occurs in some numerical columns
			#this assumes all columns not explicitly mentioned as a key column are INTEGERS
			for (a,b) in r.iteritems():
				if a != polling_station_number and a not in group_by_keys:

					try:
						combined_record[a] = int(combined_record[a])
					except ValueError:
						combined_record[a] = 0

					try:
						combined_record[a] += int(b)
					except ValueError:
						pass

			combined_record[merged_record_list_key] += r[polling_station_number]


	if debug_combine:
		print "="
		pprint(combined_record)

	new_records.append(combined_record)
	#pass

fields = new_records[0].keys()
fields.remove(merged_record_list_key)
fields.append(merged_record_list_key)

writer = csv.DictWriter(sys.stdout, fieldnames = fields)
writer.writeheader()
for r in new_records:
	writer.writerow(r)
	pass
