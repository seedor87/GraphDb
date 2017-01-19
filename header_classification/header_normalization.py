import os
from csv_read import exe_read
from pprint import pprint
import csv
from collections import defaultdict
from classification_by_entry import classification_module

local_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv', 'input.csv')
cm = classification_module()
cm.instantiate_classifier()

def has_header(file):
    temp = csv.Sniffer().has_header(file.read(2048))
    file.seek(0)
    return temp

def determine_header(entries):
    return next(cm.classify(entries[0]))

columns = defaultdict(list)
with open(local_file_path, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    if has_header(csvfile):
        next(reader)
    for row in reader:
        for i in range(len(row)):
            columns[i].append(row[i])


headers = defaultdict(basestring)
for k, v in columns.iteritems():
    headers[k] = determine_header(v)

print headers
"""
TODO write headers when necessary
"""

"""
TODO
improve the classification algorithm to be as accurate as possible
"""