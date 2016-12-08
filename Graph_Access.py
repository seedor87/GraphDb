from py2neo import Graph


class GraphManager(object):

    def __init__(self, address):
        self.graph = Graph(address)
        self.committed = []
        self.uncommitted = None
        # print self.graph.data("MATCH (a:Person) RETURN a.Name, a.age")

    def create_uncommitted(self):
        self.graph.create(self.uncommitted)
        self.committed.append(self.uncommitted)
        ret = self.committed.index(self.uncommitted)
        self.uncommitted = None
        return ret

    def add_to_uncommitted(self, subgraph):
        if self.uncommitted is not None: self.uncommitted = self.uncommitted | subgraph
        else: self.uncommitted = subgraph

    def subgraph_exists(self):
        pass

    def retrieve(self, index):
        if index < 0 or index >= len(self.committed):
            if self.uncommitted is None:
                return False # No subgraph founded
            return self.uncommitted
        else: return self.committed[index]

    def replace(self, subgraph, index):
        if index < 0 or index >= len(self.committed):
            self.uncommitted = subgraph
        else: self.committed[index] = subgraph

    def match_node(self, label, props, rlabel, elabel, eprops):
        propstr = self._prop_dict_str(props)
        label = ':'+label if label else ""
        cipher = "MATCH (m{0}{1})".format(label, propstr)
        cipher2 = " RETURN m"

        if rlabel:
            cipher+=("-[r{0}]->").format(":"+rlabel if rlabel else "")
            cipher2+=", r"

        if rlabel and elabel:
            propstr = self._prop_dict_str(eprops)
            elabel = "" if not elabel else ':'+elabel
            cipher+=("(n{0}{1})".format(elabel, propstr))
            cipher2+=", n"

        print cipher+cipher2
        print self.graph.data(cipher+cipher2)
        # {u'm': (c91495f:Person {bearing:"100",lat:"100",long:"80",name:"jason bourne",percentmatched:"99"})}
        # convert string to nodes.

    @staticmethod
    def _prop_dict_str(props):
        propstr = ','.join([x+'=' + (y if y.isdigit() else ('"'+y+'"'))
                            for x, y in props.iteritems()])
        if propstr is not "": propstr = ' {'+propstr+'}'
        return propstr