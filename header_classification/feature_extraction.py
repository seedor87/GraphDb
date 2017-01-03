
select_chars = [':', '/', '.', '1', '2', '9']

def extract_features(data):
    ret = {}
    for char in select_chars:
        ret['count: {}'.format(char)] = data.count(char)
    ret['len'] = len(data)
    return ret