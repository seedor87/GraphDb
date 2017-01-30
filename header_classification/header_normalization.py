import sys, os, csv, random, operator
from collections import defaultdict
from classification_module import classification_module, prc_slice

local_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv', 'input.csv')

class normalizer():

    def __init__(self):
        self.cm = classification_module()
        self.cm.instantiate_classifier()

    def determine_header(self, entries, shuffle=False, stop=0.1):
        """
        This method is used to encapsulate the ability to categorically decide what classification is used to make the header of the csv
        By redundantly applying the classification technique of the classification_module we can decide what class to write in as a header for the output csv

        `entries:` the list of entries of a given csv column to be classified
        `shuffle:` the optional parameter to randomize data for improved classification
        `stop`: default value is 10%, the point at which we stop parsing the entries to save runtime cycles
        """
        categories = defaultdict(int)
        if shuffle:
            random.shuffle(entries)
        _entries = prc_slice(entries, start=0.0, stop=stop)
        for classification in self.cm.classify(*_entries):
            categories[classification] += 1
        return max(categories.iteritems(), key=operator.itemgetter(1))[0]

    def exe(self, in_file_path, out_file_path=None, delimiter=','):
        """
        This method is the main executable of the functionality of this script
        By processing the existing, or non existing, header of the in file, the columns of the csv are first split.
        Then the columns of the csv are used to determine the categorized header to be written to the out file.

        `param in_file_path:` mandatory input csv file path
        `param out_file_path:` optional output file path, if None output will be written to the in file path
        `param delimiter:` optional delimiter for csv entries. default is ','
        """
        _out_file_path = in_file_path if out_file_path is None else out_file_path

        columns = defaultdict(list)
        cm = classification_module()
        cm.instantiate_classifier()

        with open(in_file_path, 'rb') as in_file:
            reader = csv.reader(in_file, delimiter=delimiter)

            # skip the row that is headers
            switch = csv.Sniffer().has_header(in_file.read(1024))
            in_file.seek(0)
            if switch:
                next(reader)

            # Build new data struct of dictionary of columns
            for row in reader:
                for i in range(len(row)):
                    columns[i].append(row[i])

            # determine what new headers will be, stored in fieldnames
            fieldnames = defaultdict(basestring)
            for k, v in columns.iteritems():
                fieldnames[k] = self.determine_header(v)
            fieldnames = fieldnames.values()

            # reconstruct rows from columns
            new_l = zip(*columns.values())

            # Write the rows one by one out to the optional out_file_path
            with open(_out_file_path, 'wb') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(fieldnames)
                for row in new_l:
                    writer.writerow(row)

if __name__ == '__main__':
    file = local_file_path
    try:
        file = sys.argv[1]
    except Exception as e:
        print 'sys argv failed,', e, 'Switching to default file path'
    print 'file:', file
    module = normalizer()
    module.exe(file)
    print 'Success'