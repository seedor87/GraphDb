import os, sys
from csv_read import exe_read
from feature_extraction import extract_features

# local file used in all testing and training
pickled_classifier_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources', 'pickled_classifier')
local_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv', 'input.csv')

"""
This lambda is used to obtain the slicing of a list using floating point values.
The start and stop parameters are used to specify the relative percentage of the list to be  sliced.
Start of 0.0 and stop of 0.25 means return the first 25% of the list. Start of 0.5 and stop of 0.55 means return the 5% of the list following the first half (50%) of the list.
And start 0.0 and stop of 1.0 means return the entire (100%) of the list.

`param list`: list to be sliced
`param start`: the starting percentage of list slice
`param stop`: the ending percentage of list slice
`return`: the list slicing.
"""
prc_slice = lambda list, start=0.0, stop=1.0: list[int(start*len(list)):int(stop*len(list))]

class classification_module():
    """
    This class holds the responsibility of rendering the classification of a given string entry.
    By relying on a pre-constructed classifier object (nltk.NaiveBayesClassifier) that is made in the make_classifier.py file and stored in the file 'pickled_classifier,' we are able to determine the classification of any given string entry.
    The accuracy of such a task relies on the strength of the classifier object that is used.
    """

    def __init__(self):
        """
        constructor for the classification module object.
        Useful only for establishing the fields that will be used in implementation.
        """
        self.classifier = None
        self.test_data = None
        self.test_set = None

    def instantiate_classifier(self, file_name=pickled_classifier_path):
        """
        This method is used only for reading the classifier to be used for task.
        Uses python's serialization suite, pickle
        Default value of param file_name is local reference predisposed by the make_classifier module.

        `file_name`: the path to the file that holds the pickled classifier
        """
        import pickle
        with open(file_name,'rb') as fileObject:
            self.classifier = pickle.load(fileObject)

    def read_test_data(self, file_path, shuffle=False, start=0.0, stop=1.0):
        """
        This method is used to read in the csv data to be used during employment.

        `file_path`: path to file to with csv data to be read in
        `shuffle`: optional, switch to random.shuffle data
        `start`: start index to be passed to prc_slice
        `stop`: stop index to be passed to prc_slice
        """
        test_data = exe_read(file_path, shuffle=shuffle)
        self.test_data = prc_slice(test_data, stop=stop, start=start)

    def classify(self, *entries):
        """
        This generator applies the constructed composite object, self.classifier, to yield determined classification.

        `strings`: the 0 or more strings to be classified
        `yield`: the classification of the associated string.
        """
        for entry in entries:
            yield self.classifier.classify(extract_features(entry))

    def dev_testing(self):
        """
        Special method for extensive developmental testing.

        `return`: num_errors, the count of erroneous classifications.
        """
        print 'DEV TESTING'

        #investigate errors of classification
        errors = []
        for data, _class in self.test_data:
            guess = next(self.classify(data))
            print 'data : {:<20} guess : {:<10} classified : {:<20}'.format(data, guess, _class)
            if guess != _class:
                errors.append((_class, guess, data))
        for _class, guess, data in sorted(errors):
            print('correct = {:<10} guess = {:<10} entry = {:<30}'.format(_class, guess, data))

        # Construct test set for later use
        self.test_set = []
        for entry, cat in self.test_data:
            feats = extract_features(entry)
            self.test_set.append((feats, cat))

        # Automated display of useful classifier features
        print self.classifier.show_most_informative_features()

        # Approx error estimation
        return len(errors)

    def run_dev_testing(self, file_path=local_file_path, test_data=None):
        """
        This method holds the dev testing staging for development

        `file_path`: file path to be read for input data to be classified
        `dev`: optional, switch for dev_testing
        """
        # demo usage
        if test_data is None:
            self.read_test_data(file_path, shuffle=True,stop=0.1)
        else:
            self.test_data = test_data
        # dev testing - all the work to do
        num_errors = self.dev_testing()

        # applied statistics for more knowledge
        len_test_set = len(self.test_set)
        accuracy = (float(len_test_set - num_errors) / len_test_set) * 100
        print 'Tests conducted: {:<6} Num. of errors: {:<6} Acc.: {:<6}%'.format(len_test_set, num_errors, accuracy)

if __name__ == '__main__':
    """
    Main method for usage and testing
    run with script example script params:
    words 07/08/94 12:12:00
    to demo contextual application
    else used for dev testing the applied classifier for constant improvement and reuse
    """
    cm = classification_module()
    cm.instantiate_classifier()
    if len(sys.argv) > 1:
        # contextual application
        entries = sys.argv[1:]
        print 'entries form script params: {:<20}'.format(entries)
        my_classifier = cm.classify(*entries)
        for elem in entries:
            print 'data: {:<20} classified: {:<10}'.format(elem, next(my_classifier))
    else:
        # dev testing
        cm.run_dev_testing(local_file_path)