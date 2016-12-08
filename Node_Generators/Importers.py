import csv
from Node_Generators import Neo_Conversion
from os.path import isfile


class Importer(object):

    def __init__(self):
        pass

    def import_file(self, pathname):
        pass


class CsvImporter(Importer):

    def import_file(self, pathname, lblkey=None):
        """Path will have csv removed prior."""
        ret = None
        builder = Neo_Conversion.NodeBuilder()
        try:
            if lblkey is None:
                with open(pathname, 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    lblkey = reader.next()[0].lower()
            with open(pathname, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    lrow = {}
                    for key, value in row.iteritems():
                        lkey = key.lower()
                        if isinstance(value, str): lvalue = value.lower()
                        lrow[lkey] = lvalue
                    row = lrow

                    if lblkey in row:  # Grab the value of the labelkey.
                        label = row[lblkey]
                        del row[lblkey]
                    else: label = lblkey
                    ret = builder.add_new_node(label, row, ret)
        except IOError:
            print "ERROR: File not found."
        return ret


class ImportFactory(object):

    def __init__(self):
        pass

    @staticmethod
    def get_importer(f):
        """Returns a object that can import the file provided or none if nothing can."""
        if not isfile(f):
            print "ERROR: That file doesn't exist."
            return None

        if f[-4:] == '.csv':
            return CsvImporter()
        else:
            print 'ERROR: No importer created for that file type.'
            return None
