from nltk.corpus import wordnet as wn
from collections import defaultdict
from pprint import pprint

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

def generator(val, steps):
    dic = {}
    total = dictify(dic, val, steps=steps)
    pprint(dic)
    print '-' * 1000
    pprint(dict([(val, total)]))


def dictify(dic, val, steps=1):
    d = {}
    if steps < 2:
        dic[val] = {}
        for meth, sets in synset_method_values(val):
            dic[val][meth] = sets
            d[meth] = sets
    else:
        dic[val] = {}
        for meth, sets in synset_method_values(val):
            dic[val][meth] = {}
            d[meth] = {}
            for set in sets:
                d[meth][set] = dictify(dic[val][meth], set, steps-1)
    return d


def get_all_words(d, list):
    for k, v in d.iteritems():
        list.add(k)
        for key, val in v.iteritems():
            if isinstance(val, dict):
                get_all_words(val, list)


val = 'WORD'
sets = wn.synsets(val)
for set in sets:
    gen = generator(set, steps=1)

# while 1:
#     try:
#         pprint(gen.next())
#         print '-' * 1000
#     except Exception as e:
#         break

# s = set()
# get_all_words(d, s)
# pprint(s)
# print len(s)

# l = set()
# get_all_words(d, l)
# print l
#
# print 'trace'
# print d['WORD']
# print d['WORD']['hypo']
# print d['WORD']['hypo']['wordA']
# print d['WORD']['hypo']['wordA']['hyper']
# print d['WORD']['hypo']['wordA']['hyper']['wordB']
# print d['WORD']['hypo']['wordA']['hyper']['wordB']['hypo']
# print d['WORD']['hypo']['wordA']['hyper']['wordB']['hypo']['wordC']
#
# print len(d)

