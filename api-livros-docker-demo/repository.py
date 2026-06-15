"""
Camada de dados (Repository).

O repository esconde COMO os dados sao guardados. O resto da API conversa
apenas com a interface RepositorioLivros, sem saber se por tras existe um
dicionario em memoria, um SQLite ou um banco remoto.

Isso e o D de SOLID (Dependency Inversion): para trocar o armazenamento,
basta criar outra implementacao de RepositorioLivros --- o service e as
rotas nao mudam nada.
"""

from abc import ABC, abstractmethod

from models import Livro, LivroCriar, LivroAtualizar


class RepositorioLivros(ABC):
    """Interface que qualquer repositorio de livros deve implementar."""

    @abstractmethod
    def listar(self) -> list[Livro]:
        ...

    @abstractmethod
    def buscar_por_id(self, livro_id: int) -> Livro | None:
        ...

    @abstractmethod
    def adicionar(self, dados: LivroCriar) -> Livro:
        ...

    @abstractmethod
    def atualizar(self, livro_id: int, dados: LivroAtualizar) -> Livro | None:
        ...

    @abstractmethod
    def remover(self, livro_id: int) -> bool:
        ...


class RepositorioEmMemoria(RepositorioLivros):
    """
    Implementacao que guarda os livros em um dicionario na memoria.

    LIMITACAO PROPOSITAL: os dados vivem apenas enquanto o servidor
    estiver no ar. Ao reiniciar, tudo se perde. Essa dor sera resolvida
    nas proximas aulas (container + deploy + persistencia externa).
    """

    def __init__(self) -> None:
        self._livros: dict[int, Livro] = {}
        self._proximo_id: int = 1

    def listar(self) -> list[Livro]:
        return list(self._livros.values())

    def buscar_por_id(self, livro_id: int) -> Livro | None:
        return self._livros.get(livro_id)

    def adicionar(self, dados: LivroCriar) -> Livro:
        novo = Livro(
            id=self._proximo_id,
            titulo=dados.titulo,
            autor=dados.autor,
            ano=dados.ano,
            isbn=dados.isbn,
        )
        self._livros[novo.id] = novo
        self._proximo_id += 1
        return novo

    def atualizar(self, livro_id: int, dados: LivroAtualizar) -> Livro | None:
        if livro_id not in self._livros:
            return None
        atualizado = Livro(
            id=livro_id,
            titulo=dados.titulo,
            autor=dados.autor,
            ano=dados.ano,
            isbn=dados.isbn,
        )
        self._livros[livro_id] = atualizado
        return atualizado

    def remover(self, livro_id: int) -> bool:
        if livro_id not in self._livros:
            return False
        del self._livros[livro_id]
        return True
