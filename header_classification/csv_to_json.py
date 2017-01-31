import csv, json, os, itertools
from collections import defaultdict

csvfile = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv', 'input.csv')
jsonfile = 'file.json'

def main():
    with open(csvfile, 'rb') as in_file, open(jsonfile, 'wb') as out_file:
        fieldnames = in_file.readline().rstrip('\n\r').split(',')
        reader = csv.reader(in_file)
        columns = defaultdict(list)
        for row in itertools.islice(reader, 100):
            for index, header in enumerate(fieldnames):
                columns[header].append(row[index])
        json.dump(columns, out_file, sort_keys=True, indent=4)

main()
