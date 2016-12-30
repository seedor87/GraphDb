import csv, datetime
from random import randrange
from pprint import pprint

startDate = datetime.datetime(1970, 9, 20, 13, 00)
select_chars = [':', '/', '.', '1', '2', '9']

def random_date(start, n):
   current = start
   while n > 0:
      curr = current + datetime.timedelta(seconds=randrange(1.57e9))
      yield curr
      n -= 1

type_formats = {'date': ["%m/%d/%Y", "%Y-%d-%m", "%d.%m.%Y"],
                'time': ["%H:%M:%S", "%H:%M"],
                'date_time': ["%d/%m/%Y %H:%M:%S"]
                }

def prc_slice(list, start, stop):
    size = len(list)
    return list[int(start*size):int(stop*size)]

size = 10000
labeled_input = {}
for k, v in type_formats.iteritems():
    labeled_input[k] = []
    for val in v:
        for x in random_date(startDate, size):
            labeled_input[k].append(x.strftime(val))
l = []
for k, v in labeled_input.iteritems():
    l.append(v)
for header, fomula in type_formats.iteritems():
    pass
new_l = zip(*l)
new_l.insert(0, tuple(labeled_input.keys()))
pprint(new_l)

spamWriter = csv.writer(open('/Users/robertseedorf/PycharmProjects/GraphDb/csv/input.csv', 'w'))

for row in new_l:
    spamWriter.writerow(row)
