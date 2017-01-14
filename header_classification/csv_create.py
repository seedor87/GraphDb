import csv, datetime, os
import random
from pprint import pprint
from faker import Faker

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

def main():

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

from faker.providers import BaseProvider

# create new provider class


if __name__ == '__main__':

    # Load the faker and its providers
    faker  = Faker()

    class MyProvider(BaseProvider):

        def balance(self):
            return faker.pydecimal(left_digits=4, right_digits=2, positive=False)

        def units(self):
            return faker.currency_code()

        def lat_lon(self):
            return random.uniform(-180, 180)

    # then add new provider to faker instance
    faker.add_provider(MyProvider)

    def test(target, lim):

        # stuff = ["name", "email", 'phone_number', "ssn", 'job'] # Person
        # stuff = ['profile'] # lengthy person profile
        # stuff = ["company", 'company_suffix', 'catch_phrase', 'bs'] # company
        # stuff = ['date_time_this_century', 'date'] # time date and date time
        # stuff = ['file_name'] # rand file
        # stuff = ['image_url', 'ipv4', 'ipv6', 'domain_name', 'url', 'company_email']
        # stuff = ['pytuple'] # garbage day
        stuff = ['balance', 'units', 'lat_lon'] # demo MyProvider

        with open(target, 'w') as o:
            writer = csv.writer(o)
            it = getattr(faker, stuff[0])()
            writer.writerow(it.keys()) if isinstance(it, dict) else writer.writerow(stuff)
            for row in range(lim):
                row = []
                for item in stuff:
                    it = getattr(faker, item)()
                    row.append(it.values()) if isinstance(it, dict) else row.append(it)
                writer.writerow(row)

    test('input.csv', 10)
