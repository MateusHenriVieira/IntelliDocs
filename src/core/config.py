from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Classe de configurações que carrega variáveis do ambiente (.env).
    """
    # Variáveis do Banco de Dados
    DATABASE_URL: str

    # Variáveis do Redis
    REDIS_HOST: str
    REDIS_PORT: int

    # Variáveis do Firebase
    FIREBASE_PROJECT_ID: str

    # Variáveis do Modelo de IA
    GROQ_API_KEY: str

    class Config:
        # Informa ao Pydantic para ler as variáveis de um arquivo .env
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Cria uma instância única das configurações que será usada em toda a aplicação.
# É este objeto 'settings' que os outros arquivos estão tentando importar.
settings = Settings()