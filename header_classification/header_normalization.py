import os, csv, random, operator
from collections import defaultdict
from classification_by_entry import classification_module, prc_slice

local_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv', 'input.csv')
cm = classification_module()
cm.instantiate_classifier()

def has_header(file_path):
    """
    TODO Fix this method it is in error now

    :param file_path:
    :return:
    """
    with open(file_path, 'rb') as file:
        temp = csv.Sniffer().has_header(file.readline())
        file.seek(0)
    return temp

def determine_header(entries, shuffle=None, stop=0.1):
    """

    """
    categories = defaultdict(int)
    if shuffle:
        random.shuffle(entries)
    _entries = prc_slice(entries, start=0.0, stop=stop)
    for classification in cm.classify(*_entries):
        categories[classification] += 1
    return max(categories.iteritems(), key=operator.itemgetter(1))[0]

def main(in_file_path, out_file_path=None, delimiter=','):

    _out_file_path = in_file_path if out_file_path is None else out_file_path

    columns = defaultdict(list)
    switch = has_header(in_file_path)
    with open(in_file_path, 'rb') as in_file:
        reader = csv.reader(in_file, delimiter=delimiter)

        # skip the row that is headers
        if switch:
            next(reader)

        # Build new data struct of dictionary of columns
        for row in reader:
            for i in range(len(row)):
                columns[i].append(row[i])

        # determine what new headers will be, stored in fieldnames
        fieldnames = defaultdict(basestring)
        for k, v in columns.iteritems():
            fieldnames[k] = determine_header(v)
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
    main(local_file_path)