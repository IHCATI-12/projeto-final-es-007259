"""
Modelos Pydantic da API de catalogo de livros.

Separamos o modelo de ENTRADA (LivroCriar / LivroAtualizar) do modelo
de SAIDA (Livro). O id e gerado pelo sistema, entao nao faz parte da
entrada --- o cliente nao escolhe o id.
"""

from pydantic import BaseModel, Field


class LivroCriar(BaseModel):
    """Dados que o cliente envia para criar um livro (sem id)."""
    titulo: str = Field(..., min_length=1, description="Titulo do livro")
    autor: str = Field(..., min_length=1, description="Nome do autor")
    ano: int = Field(..., ge=0, le=2100, description="Ano de publicacao")
    isbn: str = Field(..., min_length=1, description="Codigo ISBN")


class LivroAtualizar(BaseModel):
    """Dados que o cliente envia para atualizar um livro (sem id)."""
    titulo: str = Field(..., min_length=1)
    autor: str = Field(..., min_length=1)
    ano: int = Field(..., ge=0, le=2100)
    isbn: str = Field(..., min_length=1)


class Livro(BaseModel):
    """Livro completo, como a API devolve (com id gerado pelo sistema)."""
    id: int
    titulo: str
    autor: str
    ano: int
    isbn: str
