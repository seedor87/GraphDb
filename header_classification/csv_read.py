import csv

def use():
    test_data = []
    with open('/Users/robertseedorf/PycharmProjects/GraphDb/csv/input.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        headers = spamreader.next()
        for row in spamreader:
            test_data.extend(zip(row, headers))
            print zip(row, headers)
    print len(test_data)
    return test_data

def main():
    use()

if __name__ == '__main__':
    main()