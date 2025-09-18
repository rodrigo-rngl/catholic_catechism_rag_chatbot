from typing import Literal
from src.infra.interfaces.embedder_interface import EmbedderInterface
from src.infra.fastembed_embedder.fastembed_hybrid_embedder import FastembedHybridEmbedder

class FastembedEmbedderFactory:
    def __init__(self, search_type: Literal['Semântica', 'Esparsa', 'Híbrida']):
        self.search_type = search_type

    def produce(self) -> EmbedderInterface:
        if self.search_type == 'Híbrida':
            return FastembedHybridEmbedder()
        else:
            raise TypeError(f"Não há implementação de Embedder para o tipo de busca '{self.search_type}'.")