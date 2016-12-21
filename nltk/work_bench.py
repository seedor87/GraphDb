from nltk.corpus import wordnet as wn
from pprint import pprint

def synset_method_values(synset):
    """
    For a given synset, get all the (method_name, value) pairs
    for that synset. Returns the list of such pairs.
    """
    name_value_pairs = []
    method_names = ['hypernyms', 'instance_hypernyms', 'hyponyms', 'instance_hyponyms',
                    'member_holonyms', 'substance_holonyms', 'part_holonyms',
                    'member_meronyms', 'substance_meronyms', 'part_meronyms',
                    'attributes', 'entailments', 'causes', 'also_sees', 'verb_groups',
                    'similar_tos']
    for method_name in method_names:
        method = getattr(synset, method_name)
        vals = method()
        if not vals or vals is [] or vals is None:
            pass
        else:
            name_value_pairs.append((method_name, vals))
    return name_value_pairs

def generator(synsets, steps):
    for i in range(1, steps+1):
        total = {}
        for s in synsets:
            ret = dictify({}, s, steps=i)
            total[s] = ret
        yield total

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
            else:
                list |= set(val)

if __name__ == "__main__":
    val = None
    while 1:
        val = raw_input('Enter the word here >>> ')
        if val == 'q':
            break
        synsets = wn.synsets(val)
        generator = generator(synsets, steps=3)
        while 1:
            try:
                print "-" * 100
                output = next(generator)
                # pprint(output)
                print '- - ' * 25
                set_of_all_words = set()
                get_all_words(output, set_of_all_words)
                pprint(set_of_all_words)
                print len(set_of_all_words)

            except Exception as e:
                print e
                break