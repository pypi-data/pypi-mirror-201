"""Empty Index."""

from local_llama_index.indices.empty.base import GPTEmptyIndex
from local_llama_index.indices.empty.query import GPTEmptyIndexQuery

__all__ = [
    "GPTEmptyIndex",
    "GPTEmptyIndexQuery",
]
