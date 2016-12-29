from nltk.corpus import names
import random, nltk, datetime
from random import randrange

startDate = datetime.datetime(1970, 9, 20, 13, 00)

select_chars = [':', '/']

def random_date(start,l):
   current = start
   while l > -1:
      curr = current + datetime.timedelta(seconds=randrange(1.57e9))
      yield curr
      l-=1

def string_features(word):
    ret = {}
    for char in select_chars:
        ret['count: {}'.format(char)] = word.count(char)
    return ret

#gen input for training
labeled_input = []
for x in random_date(startDate, 50):
  labeled_input.append((x.strftime("%d/%m/%Y"), 'date'))

for x in random_date(startDate, 50):
  labeled_input.append((x.strftime("%Y-%d-%m"), 'date'))

for x in random_date(startDate, 50):
    labeled_input.append((x.strftime("%H:%M:%S"), 'time'))

for x in random_date(startDate, 50):
    labeled_input.append((x.strftime("%H:%M"), 'time'))

for x in random_date(startDate, 100):
    labeled_input.append((x.strftime("%d/%m/%Y %H:%M:%S"), 'date_time'))

# crucial to proper learning
random.shuffle(labeled_input)

train_names = labeled_input[100:]
devtest_names = labeled_input[100:200]
test_names = labeled_input[:100]

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
    next_date = next(date_gen).strftime("%d-%m-%Y")
    next_time = next(time_gen).strftime("%H:%M:%S")
    next_dt = next(dt_gen).strftime("%d/%m/%Y %H:%M:%S")
    print next_date, classifier.classify(string_features(next_date))
    print next_time, classifier.classify(string_features(next_time))
    print next_dt, classifier.classify(string_features(next_dt))

print (nltk.classify.accuracy(classifier, test_set))
print classifier.show_most_informative_features(5)

# errors = []
# for (name, tag) in devtest_names:
#     guess = classifier.classify(string_features(name))
#     if guess != tag:
#         errors.append( (tag, guess, name) )
# for (tag, guess, name) in sorted(errors):
#     print('correct={:<8} guess={:<8s} name={:<30}'.format(tag, guess, name))