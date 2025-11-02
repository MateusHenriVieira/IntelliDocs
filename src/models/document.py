from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import relationship

from src.db.base import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True, nullable=False)
    file_path = Column(String, nullable=False)  # Caminho no storage (ex: S3, local)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)
    status = Column(String, default="PENDING_PROCESSING", index=True) # PENDING, PROCESSING, COMPLETED, FAILED
    category = Column(String, nullable=True)
    tags = Column(JSON, nullable=True)
    
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    uploaded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    organization = relationship("Organization")
    uploaded_by = relationship("User")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    page_number = Column(Integer, nullable=False)
    
    
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)

    document = relationship("Document", back_populates="chunks")