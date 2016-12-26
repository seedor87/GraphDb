from nltk.corpus import wordnet as wn
from pprint import pprint

class word_relation_generator():
    """
    This class encapsulates the tools that are used to collect the paths of word relations as nested dictionaries as a mapping
    The map is used to compart_of_speeche a set of all unique entries of words that exist in the map.
    These features are leveraged to determine the major super groupings of words
    """
    def __init__(self, part_of_speech=None):
        """
        Constructor for instance of class word_relation_generator that uses params to define use
        part_of_speech (pos) can be used to specify smaller domain of words to search for mapping (range: {'v', 'n', 'a'})
        """
        self.part_of_speech = part_of_speech
    
    def key_wrap(self, synset):
        """
        Not used yet
        Can be used to gather the important features of the str() representation of nltk.corpus's synset class
        """
        _syn_set = str(synset)
        index_first_period = _syn_set.find('.')
        word = _syn_set[8:index_first_period]
        part_of_speech = _syn_set[index_first_period + 1]
        num = _syn_set[-4:-2]
        return word, part_of_speech, num
    
    def synset_method_values(self, synset, method_names=None):
        """
        This method is used to collect the tuples of method set pairs on which we define relations.
        The name_value_pairs list is the collection that holds the elements to be returned. These elements are tuples where the first value is the method used to determine the second value of the tuple; a list of words that is the result.
        If no set of words exists for the particular method, no entry is made to the result to be returned.
        """
        name_value_pairs = []
        if method_names is not None:
            _method_names = method_names
        else:
            _method_names = ['hypernyms', 'instance_hypernyms', 'hyponyms', 'instance_hyponyms',
                            'member_holonyms', 'substance_holonyms', 'part_holonyms',
                            'member_meronyms', 'substance_meronyms', 'part_meronyms',
                            'attributes', 'entailments', 'causes', 'also_sees', 'verb_groups',
                            'similar_tos']
        for method_name in _method_names:
            method = getattr(synset, method_name)
            vals = method()
            if vals:
                name_value_pairs.append((method_name, vals))
        return name_value_pairs

    def make_dictionary_all_paths(self, synsets, steps):
        """
        This method is the feature that creates the mapping of words that is the pathways from key to value.
        """
        def recurse_dictify(val, steps=1):
            """
            Recursive method that builds the mapping as value of ret.
                Pseudo:
                    while we have yet reached the limit of steps specified by user:
                        for each method, set pairing of synset_method_values for word val:
                        ret[method] = new dictionary
                        for each synset in list sets:
                            ret[method][set] = call to recurse dictify(set, steps--)
            """
            ret = {}
            if steps < 2:
                for meth, sets in self.synset_method_values(val):
                    ret[meth] = sets
            else:
                for meth, sets in self.synset_method_values(val):
                    ret[meth] = {}
                    for set in sets:
                        ret[meth][set] = recurse_dictify(set, steps-1)
            return ret

        for i in range(1, steps+1):
            total = {}  # overall dict (mapping) of all synsets and associated recursive mappings
            for s in synsets:
                total[s] = recurse_dictify(s, steps=i) # total[synset] = new mapping of all related words
            yield total

    def make_set_all_words(self, dictionary_all_paths, list):
        """
        This method is the feature that creates the set of all words in the nested mapping of the word's relations
        Note: set is of unique entries; dupes are thrown out
        """
        for k, v in dictionary_all_paths.iteritems():
            list.add(k)
            for _, sub_set in v.iteritems():
                if isinstance(sub_set, dict):
                    self.make_set_all_words(sub_set, list)
                else:
                    list |= set(sub_set)

    def generate_dictionary_all_paths(self, word, steps):
        """
        Generator for states of nested mapping of all word paths
        """
        generator = self.make_dictionary_all_paths(wn.synsets(word, pos=self.part_of_speech), steps)
        for i in range(0, steps):
            yield next(generator)

    def generate_set_all_words(self, word, steps):
        """
        Generator for the set of all words in the associated mapping
        Leverages generate_dictionary_all_paths() method to build the mapping from which the set of unique words is made
        """
        generator = self.generate_dictionary_all_paths(word, steps)
        for i in range(0, steps):
            paths = next(generator)
            set_of_all_words = set()
            self.make_set_all_words(paths, set_of_all_words)
            yield set_of_all_words

def main():
    """
    This method is example use in practical application
    """
    word, steps, part_of_speech = 'test', 3, 'n' # word is input word on which work is applied, steps is number of steps in the closure we wish to explore
    wrg = word_relation_generator(part_of_speech)
    gen = wrg.generate_set_all_words(word, steps)   # test for make set of all words, relies of gen all paths
    # gen = wrg.generate_dictionary_all_paths(word, steps) # test for only all paths
    for i in range(0, steps):
        output = next(gen)
        pprint(output)
        print len(output)   # For set of words; len is number of unique words in set
        print '=' * 1000

def debug():
    """
    DEBUG for testing
    """
    part_of_speech = None
    wrg = word_relation_generator()
    while 1:
        val = raw_input('Enter the word here >>> ')
        if val == 'q':
            break
        synsets = wn.synsets(val, pos=part_of_speech)
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
