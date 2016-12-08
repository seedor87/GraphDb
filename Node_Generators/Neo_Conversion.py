from py2neo import Node


class NodeBuilder(object):

    def __init__(self):
        pass

    def _generate(self, label, props):
        n = Node(label, **props)
        #for key, value in props.items():
        #    n[key] = value
        return n

    def make_node(self, label, props):
        return self._generate(label, props)

    def add_new_node(self, label, props, subgraph=None):
        ret = self.make_node(label, props)
        return ret if subgraph is None else ret | subgraph
