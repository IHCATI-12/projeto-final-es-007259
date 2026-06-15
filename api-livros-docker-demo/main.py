"""
API REST de catalogo de livros (FastAPI).

Estrutura em camadas:
  - Rotas (este arquivo): recebem a requisicao, chamam o service, devolvem a resposta
  - Service: regras de negocio
  - Repository (repository.py): guarda e recupera os dados

Para rodar:
  pip install fastapi uvicorn
  uvicorn main:app --reload

Documentacao interativa: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, status

from models import Livro, LivroCriar, LivroAtualizar
from repository import RepositorioEmMemoria, RepositorioLivros


# ----------------------------------------------------------------------
# Camada de servico (regras de negocio)
# ----------------------------------------------------------------------

class ServicoLivros:
    """
    Onde mora a logica de negocio. Recebe um RepositorioLivros pela
    interface --- nao sabe se e em memoria, SQLite ou outra coisa.
    """

    def __init__(self, repositorio: RepositorioLivros) -> None:
        self._repo = repositorio

    def listar(self) -> list[Livro]:
        return self._repo.listar()

    def buscar(self, livro_id: int) -> Livro | None:
        return self._repo.buscar_por_id(livro_id)

    def criar(self, dados: LivroCriar) -> Livro:
        return self._repo.adicionar(dados)

    def atualizar(self, livro_id: int, dados: LivroAtualizar) -> Livro | None:
        return self._repo.atualizar(livro_id, dados)

    def remover(self, livro_id: int) -> bool:
        return self._repo.remover(livro_id)


# ----------------------------------------------------------------------
# Montagem da aplicacao
# ----------------------------------------------------------------------

app = FastAPI(title="Catalogo de Livros", version="1.0.0")

# Injecao de dependencia simples: trocar a linha abaixo por outra
# implementacao de RepositorioLivros nao exige mudar mais nada.
servico = ServicoLivros(RepositorioEmMemoria())


# ----------------------------------------------------------------------
# Rotas (camada de API)
# ----------------------------------------------------------------------

@app.get("/livros", response_model=list[Livro])
def listar_livros():
    return servico.listar()


@app.get("/livros/{livro_id}", response_model=Livro)
def buscar_livro(livro_id: int):
    livro = servico.buscar(livro_id)
    if livro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro nao encontrado",
        )
    return livro


@app.post("/livros", response_model=Livro, status_code=status.HTTP_201_CREATED)
def criar_livro(dados: LivroCriar):
    return servico.criar(dados)


@app.put("/livros/{livro_id}", response_model=Livro)
def atualizar_livro(livro_id: int, dados: LivroAtualizar):
    livro = servico.atualizar(livro_id, dados)
    if livro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro nao encontrado",
        )
    return livro


@app.delete("/livros/{livro_id}", status_code=status.HTTP_200_OK)
def remover_livro(livro_id: int):
    removido = servico.remover(livro_id)
    if not removido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro nao encontrado",
        )
    return {"mensagem": "Livro removido com sucesso"}
