from collections import defaultdict

from prototyping_inference_engine.api.atom.atom import Atom
from prototyping_inference_engine.api.atom.set.atom_set import AtomSet
from prototyping_inference_engine.api.atom.term.term import Term


class IndexByTerm:
    def __init__(self, atom_set: AtomSet):
        index = defaultdict(set)
        for atom in atom_set:
            for t in atom.terms:
                index[t].add(atom)
        self._term_index: defaultdict[Term, frozenset[Atom]] = defaultdict(frozenset)

        for v in index:
            self._term_index[v] = frozenset(index[v])

    def atoms_by_term(self, t: Term) -> frozenset[Atom]:
        return self._term_index[t]