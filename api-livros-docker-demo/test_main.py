from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pytest
from main import app, servico

client = TestClient(app)

@pytest.fixture(autouse=True)
def limpar_banco():
    servico._repo._livros.clear()
    servico._repo._proximo_id = 1

@patch("main.httpx.AsyncClient.get")
def test_criar_livro_com_mock(mock_get):
    # 1. Preparando o Mock
    mock_resposta = MagicMock()
    mock_resposta.json.return_value = {
        "ISBN:12345": {
            "title": "Livro Fake da API",
            "authors": [{"name": "Autor Falso"}]
        }
    }
    mock_get.return_value = mock_resposta

    # Dados pra enviar na requisição
    dados_novo_livro = {
        "titulo": "Titulo Temporario",
        "autor": "Autor Temporario",
        "ano": 2024,
        "isbn": "12345"
    }

    # Fazendo a requisição no endpoint
    resposta = client.post("/livros", json=dados_novo_livro)

    assert resposta.status_code == 201
    dados_resposta = resposta.json()
    assert dados_resposta["titulo"] == "Livro Fake da API"
    assert dados_resposta["autor"] == "Autor Falso"
    assert dados_resposta["isbn"] == "12345"

@patch("main.httpx.AsyncClient.get")
def test_recusar_isbn_duplicado(mock_get):
    mock_resposta = MagicMock()
    mock_resposta.json.return_value = {
        "ISBN:9999": {"title": "Livro 1", "authors": [{"name": "Autor 1"}]}
    }
    mock_get.return_value = mock_resposta

    dados = {
        "titulo": "Livro 1",
        "autor": "Autor 1",
        "ano": 2023,
        "isbn": "9999"
    }
    
    # Cadastra o primeiro livro
    client.post("/livros", json=dados)

    # Tenta cadastrar de novo com o mesmo ISBN
    resposta = client.post("/livros", json=dados)
    
    # Confere se a API barrou e mandou o Erro 400
    assert resposta.status_code == 400
    assert "já tá cadastrado" in resposta.json()["detail"]

def test_listar_livros():
    resposta = client.get("/livros")
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)