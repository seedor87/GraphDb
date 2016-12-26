from nltk.corpus import wordnet as wn
from pprint import pprint

__meths ={
    'hypernyms': lambda s: s.hypernyms(),
    'instance_hypernyms': lambda s: s.instance_hypernyms(),
    'hyponyms': lambda s: s.hyponyms(),
    'instance_hyponyms': lambda s: s.instance_hyponyms(),
    'member_holonyms': lambda s: s.member_holonyms(),
    'substance_holonyms': lambda s: s.substance_holonyms(),
    'part_holonyms': lambda s: s.part_holonyms(),
    'member_meronyms': lambda s: s.member_meronyms(),
    'substance_meronyms': lambda s: s.substance_meronyms,
    'part_meronyms': lambda s: s.part_meronyms(),
    'attributes': lambda s: s.attributes(),
    'entailments': lambda s: s.entailments(),
    'causes': lambda s: s.causes(),
    'also_sees': lambda s: s.also_sees(),
    'verb_groups': lambda s: s.verb_groups(),
    'similar_tos': lambda s: s.similar_tos()
}

def path_similarity(source, destination):
    """
    synset1.path_similarity(synset2): Return a score denoting how similar two word senses are, based on the shortest path that connects the senses in the is-a (hypernym/hypnoym) taxonomy.
    The score is in the range 0 to 1. By default, there is now a fake root node added to verbs so for cases where previously a path could not be found---and None was returned---it should return a value.
    The old behavior can be achieved by setting simulate_root to be False. A score of 1 represents identity i.e. comparing a sense with itself will return 1.
    """
    return source.path_similarity(destination)

def wup_similarity(source, destination, simulate_root=False):
    """
    synset1.wup_similarity(synset2): Wu-Palmer Similarity: Return a score denoting how similar two word senses are, based on the depth of the two senses in the taxonomy and that of their Least Common Subsumer (most specific ancestor node). Note that at this time the scores given do _not_ always agree with those given by Pedersen's Perl implementation of Wordnet Similarity.
    The LCS does not necessarily feature in the shortest path connecting the two senses, as it is by definition the common ancestor deepest in the taxonomy, not closest to the two senses. Typically, however, it will so feature. Where multiple candidates for the LCS exist, that whose shortest path to the root node is the longest will be selected. Where the LCS has multiple paths to the root, the longer path is used for the purposes of the calculation.
    """
    return source.wup_similarity(destination, simulate_root=simulate_root)

def lowest_common_hypernym(source, destination):
    return source.lowest_common_hypernyms(destination)

def gen_closure(word, depth, method=None):

    ret = {}
    if method is not None:
        for s in wn.synsets(word):
            ret[s] = list(s.closure(__meths[method], depth=depth))
    else:
        for s in wn.synsets(word):
            ret[s] = {}
            for m in __meths.keys():
                ins = list(s.closure(__meths[m], depth=depth))
                if ins:
                    ret[s][m] = ins
    return ret

pprint(gen_closure('test', 3))

"""demo of lowest common hypernym use"""
# while 1:
#     word = raw_input('Enter the word here print  ')
#     for s in wn.synsets(word):
#         for _s in wn.synsets(word):
#             print "%s\t%s\t%s" % (s, _s, lowest_common_hypernym(s, _s))



