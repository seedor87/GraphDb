import os, csv, random, operator
from collections import defaultdict
from classification_by_entry import classification_module, prc_slice

local_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv', 'input.csv')
cm = classification_module()
cm.instantiate_classifier()

def has_header(file):
    temp = csv.Sniffer().has_header(file.readline())
    file.seek(0)
    return temp

def determine_header(entries, shuffle=None, stop=0.1):
    """
    TODO
    improve the classification algorithm to be as accurate as possible
    """
    categories = defaultdict(int)
    if shuffle:
        random.shuffle(entries)
    _entries = prc_slice(entries, start=0.0, stop=stop)
    for classification in cm.classify(*_entries):
        categories[classification] += 1
    return max(categories.iteritems(), key=operator.itemgetter(1))[0]

columns = defaultdict(list)
with open(local_file_path, 'rb') as in_file:
    reader = csv.reader(in_file, delimiter=',')

    switch = has_header(in_file)
    if switch:
        next(reader)    # skip the row that is headers
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