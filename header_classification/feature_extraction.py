
select_chars = [':', '/', '.', '1', '2', '9']

def string_features(word):
    ret = {}
    for char in select_chars:
        ret['count: {}'.format(char)] = word.count(char)
    return ret