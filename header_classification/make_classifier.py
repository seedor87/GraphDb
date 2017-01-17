import random, nltk, pickle
from feature_extraction import extract_features
from csv_read import exe_read

default_out_file_name = 'pickled_classifier'

class classifier_factory():

    def __init__(self, *input_files):
        self.input_files = input_files

    def make_classifier(self, training_data=None, out_file=None, shuffle=True):

        if training_data is None:
            input_training_data = []
            for file in self.input_files:
                input_training_data.extend(exe_read(file))
        else:
            input_training_data = training_data

        if shuffle:
            # Shuffle data to ensure improved approximation for training
            random.shuffle(input_training_data)

        train_set = [(extract_features(n), _class) for (n, _class) in input_training_data]
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        if out_file is None:
            return classifier
        fileObject = open(out_file, 'wb')
        pickle.dump(classifier,fileObject)
        fileObject.close()
        print 'Classifier Created Successfully. Pickled in file:', out_file

if __name__ == '__main__':
    # factory = classifier_factory('/Users/robertseedorf/PycharmProjects/GraphDb/csv/input.csv')
    factory = classifier_factory('C:/Users/Research/PycharmProjects/GraphDb/csv/input.csv')
    factory.make_classifier(out_file=default_out_file_name)