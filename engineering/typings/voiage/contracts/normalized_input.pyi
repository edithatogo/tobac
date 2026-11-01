from pathlib import Path
from typing import Self

class NormalizedInputBundle:
    @property
    def content_digest(self) -> str: ...
    @classmethod
    def read_ipc(cls, path: Path) -> Self: ...
    @classmethod
    def read_parquet(cls, path: Path) -> Self: ...
