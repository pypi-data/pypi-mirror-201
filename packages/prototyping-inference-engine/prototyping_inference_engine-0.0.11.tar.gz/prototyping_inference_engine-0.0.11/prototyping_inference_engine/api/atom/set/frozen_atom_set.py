from collections.abc import Iterable
from functools import cached_property
from collections.abc import Hashable
from typing import Iterator

from prototyping_inference_engine.api.atom.predicate import Predicate
from prototyping_inference_engine.api.atom.set.atom_set import AtomSet
from prototyping_inference_engine.api.atom.atom import Atom
from prototyping_inference_engine.api.atom.set.index.IndexedByTermAndPredicateAtomSet import \
    IndexedByTermAndPredicateAtomSet
from prototyping_inference_engine.api.atom.set.index.index_by_predicate import IndexByPredicate
from prototyping_inference_engine.api.atom.set.index.index_by_term import IndexByTerm
from prototyping_inference_engine.api.atom.set.index.index_by_term_and_predicate import IndexByTermAndPredicate
from prototyping_inference_engine.api.atom.set.index.indexed_by_predicate_atom_set import IndexedByPredicateAtomSet
from prototyping_inference_engine.api.atom.set.index.indexed_by_term_atom_set import IndexedByTermAtomSet
from prototyping_inference_engine.api.atom.term.constant import Constant
from prototyping_inference_engine.api.atom.term.term import Term
from prototyping_inference_engine.api.atom.term.variable import Variable
from prototyping_inference_engine.api.substitution.substitution import Substitution


class FrozenAtomSet(IndexedByTermAndPredicateAtomSet, Hashable):
    def __init__(self, iterable: Iterable[Atom] = None):
        if not iterable:
            iterable = ()
        AtomSet.__init__(self, frozenset(iterable))

    def __repr__(self) -> str:
        return "FrozenAtomSet: "+str(self)

    def __hash__(self) -> int:
        return hash(self._set)

    @cached_property
    def terms(self) -> set[Term]:
        return super().terms

    @cached_property
    def variables(self) -> set[Variable]:
        return super().variables

    @cached_property
    def constants(self) -> set[Constant]:
        return super().constants

    @cached_property
    def predicates(self) -> set[Predicate]:
        return super(FrozenAtomSet, self).predicates

    @property
    def index_by_predicate(self) -> IndexByPredicate:
        return self.index_by_term_and_predicate

    @property
    def index_by_term(self) -> IndexByTerm:
        return self.index_by_term_and_predicate

    @cached_property
    def index_by_term_and_predicate(self) -> IndexByTermAndPredicate:
        return IndexByTermAndPredicate(self)

    def match(self, atom: Atom, sub: Substitution = None) -> Iterator[Atom]:
        return self.index_by_predicate.match(atom, sub)

