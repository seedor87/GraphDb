from nltk.corpus import wordnet as wn
from pprint import pprint

# def decypher(synset):
#     word = synset[8:synset.find('.')]
#     pos = synset[synset.find('.') + 1]
#     num = synset[-4:-2]
#     print word, pos, num
#
#     if pos is 'NN' or pos is 'NNS' or pos is 'NNP' or pos is 'NNPS':
#         return word, 'n'
#     elif pos is 'VB' or pos is 'VBD' or pos is 'VBG' or pos is'VBN' or pos is 'VBP' or pos is'VBZ':
#         return word, 'v'
#     elif pos is 'JJ' or pos is 'JJS' or pos is 'JJR':
#         return word, 'a'
#     else:
#         raise Exception("Invalid pos")

def synset_method_values(synset):
    """
    For a given synset, get all the (method_name, value) pairs
    for that synset. Returns the list of such pairs.
    """
    name_value_pairs = []
    # All the available synset methods:
    method_names = ['hypernyms', 'instance_hypernyms', 'hyponyms', 'instance_hyponyms',
                    'member_holonyms', 'substance_holonyms', 'part_holonyms',
                    'member_meronyms', 'substance_meronyms', 'part_meronyms',
                    'attributes', 'entailments', 'causes', 'also_sees', 'verb_groups',
                    'similar_tos']
    for method_name in method_names:
        # Get the method's value for this synset based on its string name.
        method = getattr(synset, method_name)
        vals = method()
        if not vals or vals is [] or vals is None:
            pass
        else:
            name_value_pairs.append((method_name, vals))
    return name_value_pairs

def dictify_on_node(dict, node, path, steps=2):
    for method, sets in synset_method_values(node):
        for set in sets:
            _path = list(path)
            _path.append(method)
            key = key_wrap(set)
            if steps < 1:
                dict[key] = _path
            else:
                dict[key] = {}
                dictify_on_node(dict, set, _path, steps - 1)

def dictify_on_method(dict, syn_set, steps=3):
    for syn in syn_set:
            for method, sets in synset_method_values(syn):
                if steps < 1:
                    dict[method] = [key_wrap(s) for s in sets]
                else:
                    dict[method] = {}
                    dictify_on_method(dict[method], sets, steps - 1)

def key_wrap(syn_set):
    _syn_set = str(syn_set)
    index_first_period = _syn_set.find('.')
    word = _syn_set[8:]
    pos = _syn_set[index_first_period + 1]
    num = _syn_set[-4:-2]
    return word, pos, num

def main(key='method'):

    if key is 'method':
        while 1:
            total = {}
            dictify_on_method(total, wn.synsets(raw_input('Enter the word here >>> ')), steps=1)
            pprint(total)
    else:
        while 1:
            total = {}
            for syn_set in wn.synsets(raw_input('Enter the word here >>> ')):
                dictify_on_node(total, syn_set, [], steps=1)
            pprint(total)

def test():
    print "testing"

    total = {}
    for syn_set in wn.synsets(raw_input('Enter the word here >>> ')):
        dictify_on_node(total, syn_set, [], steps=2)
    pprint(total)

    total = {}
    dictify_on_method(total, wn.synsets(raw_input('Enter the word here >>> ')), steps=2)
    pprint(total)

    print total['hypernyms']['hyponyms']

if __name__ == '__main__':
    # main(key='node')
    test()