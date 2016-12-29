from nltk.corpus import names
import random, nltk, datetime
from random import randrange

startDate = datetime.datetime(1970, 9, 20, 13, 00)
select_chars = [':', '/', '.', '1', '2', '9']

def prc_slice(list, start, stop):
    size = len(list)
    return list[int(start*size):int(stop*size)]

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

def string_features(word):
    ret = {}
    for char in select_chars:
        ret['count: {}'.format(char)] = word.count(char)
    return ret

#gen input for training
type_formats = {('date', random_date): ["%m/%d/%Y", "%Y-%d-%m", "%d.%m.%Y"],
                ('time', random_date): ["%H:%M:%S", "%H:%M"],
                ('date_time', random_date): ["%d/%m/%Y %H:%M:%S"]}
                # ('float', random_data): []

size = 1000
labeled_input = []
for k, v in type_formats.iteritems():
    len_sub = size / len(type_formats)
    for val in v:
        for x in k[1](startDate, len_sub / len(val)):
            labeled_input.append((x.strftime(val), k[0]))

# crucial to proper learning
random.shuffle(labeled_input)

train_names = prc_slice(labeled_input, 0.0, 0.33)
devtest_names = prc_slice(labeled_input, 0.34, 0.66)
test_names = prc_slice(labeled_input, 0.67, 1)

"""
The training set is used to train the model, and the dev-test set is used to perform error analysis. The test set serves in our final evaluation of the system.
"""
train_set = [(string_features(n), _class) for (n, _class) in train_names]
devtest_set = [(string_features(n), _class) for (n, _class) in devtest_names]
test_set = [(string_features(n), _class) for (n, _class) in test_names]
classifier = nltk.NaiveBayesClassifier.train(train_set)

# testing
iterations = 5
date_gen = random_date(startDate, iterations)
time_gen = random_date(startDate, iterations)
dt_gen = random_date(startDate, iterations)

for i in range(iterations+1):
    next_date = next(date_gen).strftime("%d.%m.%Y")
    next_time = next(time_gen).strftime("%H:%M:%S")
    next_dt = next(dt_gen).strftime("%d/%m/%Y %H:%M:%S")
    print next_date, classifier.classify(string_features(next_date))
    print next_time, classifier.classify(string_features(next_time))
    print next_dt, classifier.classify(string_features(next_dt))

print nltk.classify.accuracy(classifier, test_set) * 100, '%'
print classifier.show_most_informative_features(5)

# errors = []
# for (name, tag) in devtest_names:
#     guess = classifier.classify(string_features(name))
#     if guess != tag:
#         errors.append( (tag, guess, name) )
# for (tag, guess, name) in sorted(errors):
#     print('correct={:<8} guess={:<8s} name={:<30}'.format(tag, guess, name))