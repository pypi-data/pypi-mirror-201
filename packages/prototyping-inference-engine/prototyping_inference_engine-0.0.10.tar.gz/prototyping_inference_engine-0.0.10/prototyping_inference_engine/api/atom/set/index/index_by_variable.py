from collections import defaultdict

from prototyping_inference_engine.api.atom.atom import Atom
from prototyping_inference_engine.api.atom.set.atom_set import AtomSet
from prototyping_inference_engine.api.atom.term.variable import Variable


class IndexByVariable:
    def __init__(self, atom_set: AtomSet):
        index = defaultdict(set)
        for atom in atom_set:
            for v in atom.variables:
                index[v].add(atom)
        self._index: defaultdict[Variable, frozenset[Atom]] = defaultdict(frozenset)

        for v in index:
            self._index[v] = frozenset(index[v])

    def atoms_by_variable(self, v: Variable) -> frozenset[Atom]:
        return self._index[v]
