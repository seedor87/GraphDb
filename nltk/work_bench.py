import nltk
from nltk.corpus import wordnet as wn
from pprint import pprint

class word_relation_generator():

    def __init__(self):
        """TODO"""
        pass

    class syn_wrapper(nltk.corpus.reader.wordnet.Synset):
        """TODO"""

        def __str__(self):
            print super(word_relation_generator.syn_wrapper, None).__str__()

    def synset_method_values(self, synset):
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

    def make_dictionary_all_paths(self, synsets, steps):
        for i in range(1, steps+1):
            total = {}
            for s in synsets:
                total[s] = self.recurse_dictify(s, steps=i)
            yield total

    def recurse_dictify(self, val, steps=1):
        ret = {}
        if steps < 2:
            for meth, sets in self.synset_method_values(val):
                ret[meth] = sets
        else:
            for meth, sets in self.synset_method_values(val):
                ret[meth] = {}
                for set in sets:
                    ret[meth][set] = self.recurse_dictify(set, steps - 1)
        return ret

    def make_set_all_words(self, d, list):
        for k, v in d.iteritems():
            list.add(k)
            for key, val in v.iteritems():
                if isinstance(val, dict):
                    self.make_set_all_words(val, list)
                else:
                    list |= set(val)

    def generate_dictionary_all_paths(self, word, steps):
        generator = self.make_dictionary_all_paths(wn.synsets(word), steps)
        for i in range(0, steps):
            yield next(generator)

    def generate_set_all_words(self, word, steps):
        generator = self.generate_dictionary_all_paths(word, steps)
        for i in range(0, steps):
            paths = next(generator)
            set_of_all_words = set()
            self.make_set_all_words(paths, set_of_all_words)
            yield set_of_all_words

def main():
    """
    This method demos example use in practical application
    """
    word, steps = 'test', 3
    wrg = word_relation_generator()
    gen = wrg.generate_set_all_words(word, steps)
    # gen = wrg.generate_dictionary_all_paths(word, steps)
    for i in range(0, steps):
        output = gen.next()
        pprint(output)
        print len(output)
        print '=' * 1000

def debug():
    """DEBUG for testing"""

    wrg = word_relation_generator()
    while 1:
        val = raw_input('Enter the word here >>> ')
        if val == 'q':
            break
        synsets = wn.synsets(val)
        generator = wrg.make_dictionary_all_paths(synsets, steps=3)
        while 1:
            try:
                print "-" * 100
                output = next(generator)
                pprint(output)
                print '- - ' * 25
                set_of_all_words = set()
                wrg.make_set_all_words(output, set_of_all_words)
                pprint(set_of_all_words)
                print len(set_of_all_words)
            except Exception as e:
                print e
                break

if __name__ == "__main__":
    main()
