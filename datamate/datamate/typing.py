import os

__all__ = [
    "TypePathLike",
]

TypePathLike = str | bytes | os.PathLike
