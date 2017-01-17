
import string, re

select_expressions = ['(([0-1]\d|2[0-3]):[0-5]\d:[0-5]\d)(AM|PM)?', '((0\d|1[0-2])/([0-2]\d|3[0-1])/(\d{2}|\d{4}))',
                      '(\+|\-)?(\d{2}\.\d+(N|S))', '(\+|\-)?(([0-8\d|90|1[0-7]\d|180)\.\d+(E|W))', '.+@.+\.\w+',
                      '(\()?\d{3}(\))?( )?\d{3}(-)?\d{4}(\d{4})?',
                      '((0\d|1[0-2])/([0-2]\d|3[0-1])/(\d{2}|\d{4})) (([0-1]\d|2[0-3]):[0-5]\d:[0-5]\d)(AM|PM)?']

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