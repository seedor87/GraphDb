import csv, random, os

def file_read(file_path):
    """
    Script method to read file into format necessary for future use.
    Assumes file headers have been stripped already.

    `param file_path`: the path to the file to be read
    `return`: test_data - the list of the entries' rows as tuples
    """
    test_data = []
    with open(file_path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        headers = spamreader.next()
        for row in spamreader:
            test_data.extend(zip(row, headers))
    return test_data

def exe_read(file_path, shuffle=False):
    """
    This method wraps the csv read to allow the ease of shuffling prior to return.

    `param file_path`: the path to the file to be read, passed to file_read
    `param shuffle`: optional, switch to apply random.shuffle before return
    `return`: ret - the list of the entries' rows as tuples
    """
    ret = file_read(file_path)
    if shuffle:
        random.shuffle(ret)
    return ret

if __name__ == '__main__':
    """ debugging """
    local_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv', 'input.csv')
    exe_read(local_file_path)
    print 'Success'