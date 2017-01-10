import csv, datetime, os
import random
from pprint import pprint

"""
Short script used to generate test data for the csv reading, classification building and classifier usage testing
"""

local_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv', 'input.csv')
startDate = datetime.datetime(1970, 9, 20, 13, 00)

def random_date(start, n):
   current = start
   while n > 0:
      curr = current + datetime.timedelta(seconds=random.randrange(1.57e9))
      yield curr
      n -= 1

def random_data(n):
    for _ in xrange(n):
        hex = '%012x' % random.randrange(16**12) # 12 char random string
        flt = float(random.randint(0,360))
        # dec_lat = random.random()
        # dec_lon = random.random()
        yield hex.lower(), flt

type_formats = {'date': ["%m/%d/%Y"],
                'time': ["%H:%M:%S", "%H:%M"],
                'date_time': ["%d/%m/%Y %H:%M:%S"]
                }

size = 10000
labeled_input = {}

for k, v in type_formats.iteritems():
    labeled_input[k] = []
    for val in v:
        for x in random_date(startDate, size):
            labeled_input[k].append(x.strftime(val))

headers = ['hex', 'float']
for h in headers:
    labeled_input[h] = []
for elems in random_data(size):
    paired = zip(headers, elems)
    for pair in paired:
        labeled_input[pair[0]].append(pair[1])

l = []
for k, v in labeled_input.iteritems():
    l.append(v)
new_l = zip(*l)
new_l.insert(0, tuple(labeled_input.keys()))
pprint(new_l)

spamWriter = csv.writer(open(local_file_path, 'w'))

for row in new_l:
    spamWriter.writerow(row)
