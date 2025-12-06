from typing import Literal
from functools import lru_cache
from src.infra.fastembed_embedder.fastembed_dense_embedder import FastembedDenseEmbedder
from src.infra.interfaces.fastembed_embedder_interface import FastembedEmbedderInterface
from src.infra.fastembed_embedder.fastembed_hybrid_embedder import FastembedHybridEmbedder

from src.config.logger_config import setup_logger
logger = setup_logger(name="FastembedEmbedderFactory")


class FastembedEmbedderFactory:
    def __init__(self, search_type: Literal['Semântica', 'Esparsa', 'Híbrida']) -> None:
        self.search_type = search_type

    def produce(self) -> FastembedEmbedderInterface:
        if self.search_type == 'Híbrida':
            return get_fastembed_hybrid_embedder()
        if self.search_type == 'Semântica':
            return get_fastembed_dense_embedder()

        else:
            raise TypeError(
                f"Não há implementação de Embedder para o tipo de busca '{self.search_type}'.")


@lru_cache(maxsize=1)
def get_fastembed_hybrid_embedder() -> FastembedHybridEmbedder:
    return FastembedHybridEmbedder()


@lru_cache(maxsize=1)
def get_fastembed_dense_embedder() -> FastembedDenseEmbedder:
    return FastembedDenseEmbedder()
