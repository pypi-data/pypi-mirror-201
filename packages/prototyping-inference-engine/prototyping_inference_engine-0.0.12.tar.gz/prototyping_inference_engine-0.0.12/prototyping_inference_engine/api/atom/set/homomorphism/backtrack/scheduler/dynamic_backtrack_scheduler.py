from math import inf
from collections import defaultdict, Counter

from prototyping_inference_engine.api.atom.atom import Atom
from prototyping_inference_engine.api.atom.set.atom_set import AtomSet
from prototyping_inference_engine.api.atom.set.homomorphism.backtrack.scheduler.backtrack_scheduler import BacktrackScheduler
from prototyping_inference_engine.api.atom.set.index.IndexedAtomSet import IndexedAtomSet
from prototyping_inference_engine.api.atom.set.index.index_by_term import IndexByTerm
from prototyping_inference_engine.api.atom.set.index.index_by_term_and_predicate import IndexByTermAndPredicate
from prototyping_inference_engine.api.atom.set.index.indexed_by_term_atom_set import IndexedByTermAtomSet
from prototyping_inference_engine.api.atom.set.mutable_atom_set import MutableAtomSet
from prototyping_inference_engine.api.atom.term.variable import Variable
from prototyping_inference_engine.api.substitution.substitution import Substitution


class DynamicBacktrackScheduler(BacktrackScheduler):
    def __init__(self, from_atom_set: AtomSet):
        BacktrackScheduler.__init__(self, from_atom_set)
        self._order = []
        self._not_ordered = set(from_atom_set)

        if isinstance(from_atom_set, IndexedAtomSet):
            self._index = from_atom_set.index
        else:
            self._index = IndexByTermAndPredicate(from_atom_set)

    def has_next_atom(self, level: int) -> bool:
        return level < len(self._order) + len(self._not_ordered)

    def next_atom(self, sub: Substitution, level: int) -> Atom:
        while level+1 < len(self._order):
            self._not_ordered.add(self._order.pop())
        if level+1 == len(self._order):
            return self._order[level]

        next_a = None
        smallest = inf
        for a in self._not_ordered:
            size = self._index.domain_size(a, sub)
            if smallest > size:
                next_a = a
                smallest = size

        self._order.append(next_a)
        self._not_ordered.remove(next_a)

        return self._order[level]
