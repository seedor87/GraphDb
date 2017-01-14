import nltk, os, sys
from csv_read import exe_read
from feature_extraction import extract_features

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

    def instantiate_classifier(self, file_name='pickled_classifier'):
        """
        This method is used only for reading the classifier to be used for task.
        Uses python's serialization suite, pickle
        Default value of param file_name is local reference predisposed by the make_classifier module.

        `param file_name`: the path to the file that holds the pickled classifier
        """
        import pickle
        with open(file_name,'rb') as fileObject:
            self.classifier = pickle.load(fileObject)

    def read_test_data(self, file_path, shuffle=False, start=0.0, stop=1.0):
        """
        This method is used to read in the csv data to be used during employment.

        `param file_path`: path to file to with csv data to be read in
        `param shuffle`: optional, switch to random.shuffle data
        `param start`: start index to be passed to prc_slice
        `param stop`: stop index to be passed to prc_slice
        """

        # file_path = '/Users/robertseedorf/PycharmProjects/GraphDb/csv/input.csv'
        test_data = exe_read(file_path, shuffle=shuffle)
        self.test_data = prc_slice(test_data, stop=stop, start=start)

    def classify(self, *entries):
        """
        This generator applies the constructed composite object, self.classifier, to yield determined classification.

        `param strings`: the 0 or more strings to be classified
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
            if guess != _class:
                errors.append((_class, guess, data))
        for _class, guess, data in sorted(errors):
            print('correct = {:<10} guess = {:<10} entry = {:<30}'.format(_class, guess, data))

        # Construct test set for later use
        self.test_set = []
        for entry, cat in self.test_data:
            feats = extract_features(entry)
            self.test_set.append((feats, cat))
        print 'Accuracy:\t{}%'.format(nltk.classify.accuracy(self.classifier, self.test_set) * 100)

        # Automated display of useful classifier features
        print self.classifier.show_most_informative_features()

        # Approx error estimation
        num_errors = len(errors)
        print '# of errors:\t{}'.format(num_errors)
        return num_errors

    def run(self, file_path, dev=None):
        """
        This method holds the example usage for one run of the program as seen fit.

        `param file_path`: file path to be read for input data to be classified
        `param dev`: optional, switch for dev_testing
        """
        # demo usage
        self.instantiate_classifier()
        self.read_test_data(file_path, shuffle=1,stop=0.1)
        if dev:
            num_errors = self.dev_testing() # dev testing - all the work to do
            print 'Tests conducted:{}'.format(len(self.test_set))
        else:
            print 'APPLIED USAGE' # example deployment
            for entry, cat in self.test_data:
                res = next(self.classify(entry))
                print 'data = {:<20} guess = {:<10} category = {:<20}'.format(entry, res, cat)

if __name__ == '__main__':
    # main for execution, for usage see the workings of run method
    cm = classification_module()
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv', 'input.csv')
    try:
        demo = sys.argv[1]
        cm.instantiate_classifier()
        entries = ['words', '07/08/94', '12:12:00']
        cl = cm.classify(*entries)
        for elem in entries:
            print elem, next(cl)
    except Exception as e:
        cm.run(file_path, dev=1)