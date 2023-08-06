from collections import defaultdict
from typing import Iterator

from prototyping_inference_engine.api.atom.atom import Atom
from prototyping_inference_engine.api.atom.set.atom_set import AtomSet
from prototyping_inference_engine.api.atom.set.index.index_by_predicate import IndexByPredicate
from prototyping_inference_engine.api.atom.set.index.index_by_term import IndexByTerm
from prototyping_inference_engine.api.atom.term.constant import Constant
from prototyping_inference_engine.api.substitution.substitution import Substitution


class IndexByTermAndPredicate(IndexByTerm, IndexByPredicate):
    def __init__(self, atom_set: AtomSet):
        IndexByTerm.__init__(self, atom_set)
        IndexByPredicate.__init__(self, atom_set)

    def match(self, atom: Atom, sub: Substitution = None) -> Iterator[Atom]:
        if sub is None:
            sub = Substitution()

        for a in self._smallest_domain(atom, sub):
            if Substitution.specialize(atom, a, sub) is not None:
                yield a

    def _smallest_domain(self, atom: Atom, sub: Substitution) -> frozenset[Atom]:
        smallest_domain = self.atoms_by_predicate(atom.predicate)
        for t in atom.terms:
            if ((isinstance(t, Constant) and len(self.atoms_by_term(t)) < len(smallest_domain))
                    or (t in sub.domain and len(self.atoms_by_term(sub(t))) < len(smallest_domain))):
                smallest_domain = self.atoms_by_term(sub(t))
        return smallest_domain

    def extend_substitution(self, atom: Atom, sub: Substitution) -> Iterator[Substitution]:
        for a in self._smallest_domain(atom, sub):
            spec = Substitution.specialize(atom, a, sub)
            if spec is not None:
                yield spec
