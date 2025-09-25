from typing import Literal
from functools import lru_cache
from src.infra.interfaces.embedder_interface import EmbedderInterface
from src.errors.types.class_not_implemented_error import ClassNotImplementedError
from src.infra.fastembed_embedder.fastembed_hybrid_embedder import FastembedHybridEmbedder

from src.config.logger_config import setup_logger
logger = setup_logger(name="FastembedEmbedderFactory")


class FastembedEmbedderFactory:
    def __init__(self, search_type: Literal['Semântica', 'Esparsa', 'Híbrida']):
        self.search_type = search_type

    def produce(self) -> EmbedderInterface:
        if self.search_type == 'Híbrida':
            return get_fastembed_hybrid_embedder()
        else:
            raise ClassNotImplementedError(
                f"Não há implementação de Embedder para o tipo de busca '{self.search_type}'.")


@lru_cache(maxsize=1)
def get_fastembed_hybrid_embedder() -> FastembedHybridEmbedder:
    return FastembedHybridEmbedder()
