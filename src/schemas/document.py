# src/models/document.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, JSON, Text
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from src.db.base import Base

class Document(Base):
    """
    Modelo SQLAlchemy para a tabela 'documents'.
    Armazena os metadados de alto nível de um arquivo enviado.
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True, nullable=False)
    file_path = Column(String, nullable=False)  # Caminho no storage (ex: S3 ou local)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)
    
    # Status do processamento de IA: PENDING_PROCESSING, PROCESSING, COMPLETED, FAILED
    status = Column(String, default="PENDING_PROCESSING", index=True)
    
    category = Column(String, nullable=True) # A ser preenchido pela IA
    tags = Column(JSON, nullable=True) # A ser preenchido pela IA
    
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    uploaded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos com outras tabelas
    organization = relationship("Organization")
    uploaded_by = relationship("User")
    
    # Relacionamento com os 'chunks'
    # 'cascade="all, delete-orphan"' significa que se um Documento for deletado,
    # todos os seus DocumentChunks associados também serão deletados.
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    """
    Modelo SQLAlchemy para a tabela 'document_chunks'.
    Armazena os pedaços de texto extraídos do documento, suas páginas
    e seus vetores de embedding correspondentes.
    """
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    
    # Usamos 'Text' em vez de 'String' para acomodar textos longos
    content = Column(Text, nullable=False) 
    
    # A "memória" da página de onde este chunk foi extraído
    page_number = Column(Integer, nullable=False)
    
    # A coluna de vetor para a busca semântica (IA)
    # O tamanho (384) deve corresponder ao modelo de embedding que estamos usando
    # (paraphrase-multilingual-MiniLM-L12-v2 tem 384 dimensões)
    embedding = Column(Vector(384), nullable=True) 
    
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    
    # Relacionamento de volta para o Documento principal
    document = relationship("Document", back_populates="chunks")