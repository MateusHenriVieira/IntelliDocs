from fastapi import FastAPI
# 1. Importe o novo módulo
from src.api.v1.endpoints import auth, users, documents, search 

app = FastAPI(
    title="IntelliDocs AI - API",
    description="Backend da plataforma IntelliDocs AI para gerenciamento inteligente de documentos.",
    version="1.0.0"
)

# 2. Inclua o novo roteador na aplicação
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(search.router, prefix="/api/v1/search", tags=["Search"]) # <<< ADICIONE ESTA LINHA


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to IntelliDocs AI API!"}