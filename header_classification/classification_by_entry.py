import nltk, pickle
from csv_read import exe_read
from feature_extraction import extract_features

def prc_slice(list, start=0.0, stop=1.0):
    size = len(list)
    return list[int(start*size):int(stop*size)]

class classification_module():

    def __init__(self):
        self.classifier = None
        self.test_data = None
        self.test_set = None

    def read_classifier(self, file_name):

        # file_name = 'pickled_classifier'
        fileObject = open(file_name,'rb')
        self.classifier = pickle.load(fileObject)
        fileObject.close()

    def read_test_data(self, file_path, shuffle=False, start=0.0, stop=1.0):

        # file_path = '/Users/robertseedorf/PycharmProjects/GraphDb/csv/input.csv'
        test_data = exe_read(file_path, shuffle=shuffle)
        self.test_data = prc_slice(test_data, stop=stop, start=start)

    def classify(self, *strings):
        for str in strings:
            yield(self.classifier.classify(extract_features(str)))

    def dev_testing(self):
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

        print self.classifier.show_most_informative_features()

        num_errors = len(errors)
        print '# of errors:\t{}'.format(num_errors)
        return num_errors

    def run(self, file_path, dev=None):
        # demo usage
        self.read_classifier('pickled_classifier')
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
    cm = classification_module()
    # file_path = '/Users/robertseedorf/PycharmProjects/GraphDb/csv/input.csv'
    file_path = 'C:/Users/Research/PycharmProjects/GraphDb/csv/input.csv'
    cm.run(file_path, dev=1)