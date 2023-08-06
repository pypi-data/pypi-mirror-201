"""Init params."""

# TODO: move LLMPredictor to this folder
from local_llama_index.llm_predictor.base import LLMPredictor
from local_llama_index.llm_predictor.structured import StructuredLLMPredictor

__all__ = [
    "LLMPredictor",
    "StructuredLLMPredictor",
]
