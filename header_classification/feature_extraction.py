import string, re

"""
This file is used to fulfill the requirements of automated pattern recognition throughout.
By exposing a variety of features to the classifier factory, an improved classifier can be created.
These features are all contained in the body of the extract_features method. This method returns the dictionary (mapping) of developed metrics to be used during classification and classifier building.
These features have been developed for use with the most broad spectrum of input we could conceive. each value is mapped to key for reference by the classifier metric analyzation suite of dev testing.

By housing this work in a separate file, the work becomes a shared resource. This is used predominantly by the make classifier and classification by entry files.

As a prerequisite of training and development, the shared resources of the classifier object being used (see the pickled classifier file) and the method of this file should hold the same state across tests.
As such all work conducted for testing must be conducted in the following manner in order to uphold the highest level of accuracy and fidelity in training, testing and deployment.
When this file is changed, a new classifier object must be made.
During this process, the new classifier is written to the pickled classifier file.
From there, further testing by application of the dev test suite in the classification by entry module maybe conducted.

"""
select_chars = [':', '/', '.', '1', '2', '9', '0']

# Implementing the regular expressions into the feature extractor. This will increase the accuracy of the
# learner to recognize these formats as the different categories.
select_expressions = ['(([0-1]\d|2[0-3]):[0-5]\d:[0-5]\d)(AM|PM)?',
                      '((0\d|1[0-2])(/|-)([0-2]\d|3[0-1])(/|-)(\d{2}|\d{4})|' +
                      '([0-2]\d|3[0-1])(/|-)(0\d|1[0-2])(/|-)(\d{2}|\d{4}))',
                      '((0\d|1[0-2])(/|-)([0-2]\d|3[0-1])(/|-)(\d{2}|\d{4})|' +
                      '([0-2]\d|3[0-1])(/|-)(0\d|1[0-2])(/|-)(\d{2}|\d{4})) ' +
                      '(([0-1]\d|2[0-3]):[0-5]\d:[0-5]\d)(AM|PM)?',
                      '^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)', '[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)', '.+@.+\.\w+',
                      '(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})']

# compares the above stated regular expressions with the data from the CSV file. If there is a match, it
# stores a 1, else it stores a 0
def extract_features(data):
    ret = {}
    for pattern in select_expressions:
        expression = re.compile(pattern)
        # if expression.match(data):
        if re.search(expression, data):
            ret['entry match at: {}'.format(pattern)] = 1
        else:
            ret['entry match at: {}'.format(pattern)] = 0
    ret['len'] = len(data)
    return ret
