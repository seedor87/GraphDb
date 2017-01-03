import cmd
import re
from Node_Generators.Importers import ImportFactory
import sys
import Graph_Access

class Console(cmd.Cmd):

    def __init__(self, address):
        cmd.Cmd.__init__(self)
        self.manager = Graph_Access.GraphManager(address)

        self.subgraph = None
        self.subindex = None

    def do_load(self,data):
        f, other = self._split_path_data(data)
        importer = ImportFactory.get_importer(f)
        if importer is not None:
            self.manager.add_to_uncommitted(importer.import_file(f, other))

    def do_create(self, _):
        self.manager.create_uncommitted()

    def do_print(self, line):
        if line.isdigit(): line = int(line)
        else: line = -1

        sub = self.manager.retrieve(line)
        if sub is False: print "ERROR: No subgraph found."
        else:
            for x in sub.nodes():
                print x
            for x in sub.relationships():
                print x

    def do_set(self, line):
        if line.isdigit(): line = int(line)
        else: line = -1

        if self._set_graph_exists():  # save possible changes
            self.manager.committed[self.subindex] = self.subgraph
        self.subgraph = self.manager.retrieve(line)
        self.subindex = line

    def do_find(self, _):
        label, props = self._ask_node()
        rlabel = ""
        elabel, eprops = "", {}

        n = raw_input("\nAdd a relationship? Newline to finish.> ")
        if (n != ""):
            rlabel = n
            elabel, eprops = self._ask_node()

        self.manager.match_node(label, props, rlabel, elabel, eprops)

    @staticmethod
    def _ask_node():
        props = {}
        while True:
            label = raw_input("Input label to search with > ")
            if label != "": break

        key = "init"
        while key is not "":
            key = raw_input("Input property key to search with, newline to finish > ")
            if key is not "":
                val = raw_input("Input property value to search with > ")
                props[key] = val
        return label, props

    def _set_graph_exists(self):
        if self.subgraph is None:
            return False
        return True

    @staticmethod
    def _split_path_data(data):
        r = re.match("([^.]*\..{3}) (.*)", data)
        return r.groups() if r else (data, None)

if __name__ == "__main__":
    c = Console(sys.argv[1])
    c.cmdloop()
