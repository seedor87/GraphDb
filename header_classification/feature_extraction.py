
import string, re

select_expressions = ['(([0-1]\d|2[0-3]):[0-5]\d:[0-5]\d)(AM|PM)?',
                      '((0\d|1[0-2])(/|-)([0-2]\d|3[0-1])(/|-)(\d{2}|\d{4})|' +
                      '([0-2]\d|3[0-1])(/|-)(0\d|1[0-2])(/|-)(\d{2}|\d{4}))',
                      '((0\d|1[0-2])(/|-)([0-2]\d|3[0-1])(/|-)(\d{2}|\d{4})|' +
                      '([0-2]\d|3[0-1])(/|-)(0\d|1[0-2])(/|-)(\d{2}|\d{4})) ' +
                      '(([0-1]\d|2[0-3]):[0-5]\d:[0-5]\d)(AM|PM)?',
                      '^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)', '[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)', '.+@.+\.\w+',
                      '(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})']

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
