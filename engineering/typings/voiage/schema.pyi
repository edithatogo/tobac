from collections.abc import Sequence
from typing import Self
from numpy.typing import ArrayLike

class ValueArray:
    @classmethod
    def from_numpy(cls, values: ArrayLike, strategy_names: Sequence[str] | None = ...) -> Self: ...
