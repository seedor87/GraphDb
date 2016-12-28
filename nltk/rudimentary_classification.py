from nltk.corpus import names
import random, nltk
from nltk.corpus import cmudict

d = cmudict.dict()

def nsyl(word):
   return [len(list(y for y in x if unicode.isnumeric(y[-1]))) for x in d[word.lower()]]

labeled_names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])

def gender_features(word):
    return {'suffix1': word[-1:],
            'suffix2': word[-2:]}

random.shuffle(labeled_names)

train_names = labeled_names[1500:]
devtest_names = labeled_names[500:1500]
test_names = labeled_names[:500]

"""
The training set is used to train the model, and the dev-test set is used to perform error analysis. The test set serves in our final evaluation of the system.
"""
train_set = [(gender_features(n), gender) for (n, gender) in train_names]
devtest_set = [(gender_features(n), gender) for (n, gender) in devtest_names]
test_set = [(gender_features(n), gender) for (n, gender) in test_names]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print classifier.classify(gender_features('Neo'))
print classifier.classify(gender_features('Alexandra'))
print classifier.classify(gender_features('Alex'))
print classifier.classify(gender_features('Al'))
print classifier.classify(gender_features('Eliakah'))
print (nltk.classify.accuracy(classifier, test_set))
print classifier.show_most_informative_features(5)

errors = []
for (name, tag) in devtest_names:
    guess = classifier.classify(gender_features(name))
    if guess != tag:
        errors.append( (tag, guess, name) )
for (tag, guess, name) in sorted(errors):
    print('correct={:<8} guess={:<8s} name={:<30}'.format(tag, guess, name))