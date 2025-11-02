# Dockerfile

# --- Estágio 1: Imagem Base ---
# Começamos com uma imagem oficial e leve do Python.
# Usar uma versão específica (ex: 3.11) garante consistência.
FROM python:3.11-slim

# --- Estágio 2: Configuração do Ambiente ---
# Variáveis de ambiente para otimizar a execução de Python em containers.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho padrão dentro do container.
WORKDIR /app

# --- Estágio 3: Instalação das Dependências ---
# Copia APENAS o arquivo de requisitos primeiro.
# Isso aproveita o cache do Docker: se o arquivo não mudar, as dependências
# não serão reinstaladas em builds futuros, acelerando o processo.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# --- Estágio 4: Cópia do Código da Aplicação ---
# Agora, copia o restante do código do seu projeto para o container.
# Copiamos a pasta 'src' e os arquivos de configuração do Alembic.
COPY ./src /app/src
COPY alembic.ini .
COPY alembic ./alembic

# --- Estágio 5: Execução ---
# Expõe a porta 8000, informando ao Docker que a aplicação
# escutará nesta porta.
EXPOSE 8000

# O comando para iniciar a aplicação quando o container for executado.
# O uvicorn é o servidor que roda nosso código FastAPI.
# A flag '--reload' é ótima para desenvolvimento, pois reinicia o servidor
# automaticamente quando você altera o código.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]