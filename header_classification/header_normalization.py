import os
import csv
from collections import defaultdict
from classification_by_entry import classification_module

local_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv', 'input.csv')
cm = classification_module()
cm.instantiate_classifier()

def has_header(file):
    temp = csv.Sniffer().has_header(file.readline())
    file.seek(0)
    return temp

def determine_header(entries):
    """
    TODO
    improve the classification algorithm to be as accurate as possible
    """
    return next(cm.classify(entries[0]))

columns = defaultdict(list)
with open(local_file_path, 'rb') as in_file:
    reader = csv.reader(in_file, delimiter=',')

    switch = has_header(in_file)
    if switch:
        next(reader)
    hold_over = []
    for row in reader:
        hold_over.append(row)
        for i in range(len(row)):
            columns[i].append(row[i])

    headers = defaultdict(basestring)
    for k, v in columns.iteritems():
        headers[k] = determine_header(v)
    headers = headers.values()

with open(local_file_path, 'wb') as out_file:
    writer = csv.writer(out_file)
    writer.writerow(headers)
    for row in hold_over:
        writer.writerow(row)