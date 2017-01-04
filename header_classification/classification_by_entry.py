import random, nltk, pickle
from csv_read import exe_read
from feature_extraction import extract_features

def prc_slice(list, stop, start=None):
    if start is None:
        _start = 0.0
    else:
        _start = start
    size = len(list)
    return list[int(_start*size):int(stop*size)]

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

    def read_test_data(self, file_path, start=None, stop=1.0):

        # file_path = '/Users/robertseedorf/PycharmProjects/GraphDb/csv/input.csv'
        test_data = exe_read(file_path)
        self.test_data = prc_slice(test_data, stop=stop, start=start)

    def build_test_set(self):
        self.test_set = []
        for entry, cat in self.test_data:
            feats = extract_features(entry)
            self.test_set.append((feats, cat))

    def dev_testing(self):
        print 'DEV TESTING'

        errors = []
        for (name, tag) in self.test_data:
            guess = self.classifier.classify(extract_features(name))
            if guess != tag:
                errors.append( (tag, guess, name) )
        for (tag, guess, name) in sorted(errors):
            print('correct = {:<10} guess = {:<10} entry = {:<30}'.format(tag, guess, name))

        print '# of errors:\t{}'.format(len(errors))

        print 'Accuracy:\t{}%'.format(nltk.classify.accuracy(self.classifier, self.test_set) * 100)

        print self.classifier.show_most_informative_features()

    def run(self, file_path, dev=None):
        # demo usage
        self.read_classifier('pickled_classifier')
        self.read_test_data(file_path, stop=0.3)
        if dev:
            random.shuffle(self.test_data)
            self.build_test_set()
            self.dev_testing() # dev testing - all the work to do
            print 'Tests conducted:{}'.format(len(self.test_set))
        else:
            print 'APPLIED USAGE' # example deployment
            for entry, cat in self.test_data:
                feats = extract_features(entry)
                print 'data = {:<20} guess = {:<10} category = {:<20}'.format(entry, self.classifier.classify(feats), cat)

if __name__ == '__main__':
    cm = classification_module()
    file_path = '/Users/robertseedorf/PycharmProjects/GraphDb/csv/input.csv'
    cm.run(file_path, dev=1)