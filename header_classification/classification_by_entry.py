import random, nltk, datetime, pickle
from random import randrange
from csv_read import exe
from feature_extraction import string_features

startDate = datetime.datetime(1970, 9, 20, 13, 00)
select_chars = [':', '/', '.', '1', '2', '9']

def prc_slice(list, stop, start=None):
    if start is None:
        _start = 0.0
    else:
        _start = start
    size = len(list)
    return list[int(_start*size):int(stop*size)]

def random_date(start, n):
   current = start
   while n > -1:
      curr = current + datetime.timedelta(seconds=randrange(1.57e9))
      yield curr
      n -= 1

def random_data(n, lat=0.0, lon=0.0):
    for _ in xrange(n):
        hex1 = '%012x' % random.randrange(16**12) # 12 char random string
        flt = float(random.randint(0,100))
        yield flt
        # dec_lat = random.random()/100
        # dec_lon = random.random()/100
        # yield hex1.lower(), flt, lon+dec_lon, lat+dec_lat

"""

#gen input for training
type_formats = {('date', random_date): ["%m/%d/%Y", "%Y-%d-%m", "%d.%m.%Y"],
                ('time', random_date): ["%H:%M:%S", "%H:%M"],
                ('date_time', random_date): ["%d/%m/%Y %H:%M:%S"]}
                # ('float', random_data): []

size = 10000
labeled_input = []
for k, v in type_formats.iteritems():
    len_sub = size / len(type_formats)
    for val in v:
        for x in k[1](startDate, len_sub / len(val)):
            labeled_input.append((x.strftime(val), k[0]))
"""

# we open the file for reading
file_Name = 'pickled_classifier'
fileObject = open(file_Name,'rb')
classifier = pickle.load(fileObject)
fileObject.close()

# testing
# iterations = 5
# date_gen = random_date(startDate, iterations)
# time_gen = random_date(startDate, iterations)
# dt_gen = random_date(startDate, iterations)
#
# for i in range(iterations+1):
#     next_date = next(date_gen).strftime("%d.%m.%Y")
#     next_time = next(time_gen).strftime("%H:%M:%S")
#     next_dt = next(dt_gen).strftime("%d/%m/%Y %H:%M:%S")
#     print next_date, classifier.classify(string_features(next_date))
#     print next_time, classifier.classify(string_features(next_time))
#     print next_dt, classifier.classify(string_features(next_dt))

test_data = exe()
test_data = prc_slice(test_data, stop=0.20)

test_set = []
for data, cat in test_data:
    feats = string_features(data)
    print 'data = {:<20} guess = {:<10} category = {:<20}'.format(data, classifier.classify(feats), cat)
    test_set.append((feats, cat))

print 'Tests conducted:', len(test_set)

print '-' * 100
print 'Accuracy: {}%'.format(nltk.classify.accuracy(classifier, test_set) * 100)
print classifier.show_most_informative_features()

errors = []
for (name, tag) in test_data:
    guess = classifier.classify(string_features(name))
    if guess != tag:
        errors.append( (tag, guess, name) )
for (tag, guess, name) in sorted(errors):
    print('correct = {:<10} guess = {:<10} entry = {:<30}'.format(tag, guess, name))