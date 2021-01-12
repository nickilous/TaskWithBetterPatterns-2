from typing import Hashable, TypeVar
T = TypeVar("T")

class Identifiable(Hashable):
    id: T
    def __init__(self, id: T) -> None:
        super().__init__()
        self.id = id

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, o) -> bool:
        if isinstance(o, Identifiable):
            return self.id == o.id
        return NotImplemented