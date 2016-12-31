import random, nltk, pickle
from feature_extraction import string_features
from csv_read import exe

def prc_slice(list, start, stop):
    size = len(list)
    return list[int(start*size):int(stop*size)]

file_Name = 'pickled_classifier'

input_data = exe()
random.shuffle(input_data)

train_data = prc_slice(input_data, 0.0, 0.33)
devtest_data = prc_slice(input_data, 0.34, 0.66)
test_data = prc_slice(input_data, 0.67, 1)

# The training set is used to train the model, and the dev-test set is used to perform error analysis. The test set serves in our final evaluation of the system.
train_set = [(string_features(n), _class) for (n, _class) in train_data]
devtest_set = [(string_features(n), _class) for (n, _class) in devtest_data]
# test_set = [(string_features(n), _class) for (n, _class) in test_data]

# file_Name = 'pickled_classifier'

classifier = nltk.NaiveBayesClassifier.train(train_set)

# pickle the classifier?
# open the file for writing

fileObject = open(file_Name,'wb')

# this writes the object a to the
# file named 'testfile'
pickle.dump(classifier,fileObject)

# here we close the fileObject
fileObject.close()
