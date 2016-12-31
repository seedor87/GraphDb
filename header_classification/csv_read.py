import csv, sys

local_file_path = '/Users/robertseedorf/PycharmProjects/GraphDb/csv/input.csv'

def file_read(file_path):
    test_data = []
    with open(file_path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        headers = spamreader.next()
        for row in spamreader:
            test_data.extend(zip(row, headers))
            print test_data[-1]
            # sys.stdout.write('.')
    return test_data

def exe(file_path=None):
    if file_path is None:
        _file_path = local_file_path
    else:
        _file_path = file_path
    return file_read(_file_path)

if __name__ == '__main__':
    exe()