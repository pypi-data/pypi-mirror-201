from abc import abstractmethod

from prototyping_inference_engine.api.atom.set.atom_set import AtomSet
from prototyping_inference_engine.api.atom.set.index.index_by_variable import IndexByVariable


class IndexedByVariableAtomSet(AtomSet):
    @property
    @abstractmethod
    def index_by_variable(self) -> IndexByVariable:
        pass
