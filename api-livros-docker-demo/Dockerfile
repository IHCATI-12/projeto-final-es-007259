# Dockerfile da API de catalogo de livros
#
# Ordem das instrucoes pensada para aproveitar o cache de layers:
# copiar e instalar dependencias ANTES de copiar o codigo faz com que
# mudar o codigo nao invalide a camada de instalacao das dependencias.

# 1. Imagem base com Python ja instalado (variante slim = mais leve)
FROM python:3.11-slim

# 2. Pasta de trabalho dentro da imagem
WORKDIR /app

# 3. Copiar so o requirements primeiro e instalar (camada cacheavel)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar o codigo da aplicacao
COPY . .

# 5. Documentar a porta que a aplicacao usa
EXPOSE 8000

# 6. Comando que sobe a API quando o container inicia
#    host 0.0.0.0 e necessario para aceitar conexoes de fora do container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
