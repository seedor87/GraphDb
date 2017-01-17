import csv, random

# local_file_path = '/Users/robertseedorf/PycharmProjects/GraphDb/csv/input.csv'
local_file_path = 'C:/Users/Research/PycharmProjects/GraphDb/csv/input.csv'

def file_read(file_path):
    test_data = []
    with open(file_path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        headers = spamreader.next()
        for row in spamreader:
            test_data.extend(zip(row, headers))
    return test_data

def exe_read(file_path, shuffle=False):
    ret = file_read(file_path)
    if shuffle:
        random.shuffle(ret)
    return ret

if __name__ == '__main__':
    # debugging
    exe_read(local_file_path)
    print 'Success'