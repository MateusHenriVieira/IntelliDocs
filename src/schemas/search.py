from pydantic import BaseModel
from typing import List

class SearchQuery(BaseModel):
    """
    Schema para a consulta de busca enviada pelo frontend.
    """
    query: str
    top_k: int = 5  # Quantos resultados retornar (default 5)


class SearchResultChunk(BaseModel):
    """
    Schema para um único chunk de resultado.
    """
    document_id: int
    page_number: int
    content: str
    similarity: float # Quão relevante é o resultado (0.0 a 1.0)

    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    """
    Schema para a resposta completa da busca.
    """
    results: List[SearchResultChunk]