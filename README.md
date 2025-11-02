# 🚀 IntelliDocs AI SaaS

<div align="center">

**Plataforma SaaS de Digitalização, Gerenciamento e Análise Inteligente de Documentos**

[![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)

</div>

---

## 📋 Sobre o Projeto

**IntelliDocs AI** é uma plataforma SaaS de ponta, projetada para digitalização, gerenciamento e análise inteligente de documentos. A solução é voltada para **grandes corporações** e **entidades governamentais** (prefeituras) que precisam organizar grandes volumes de documentos e extrair informações valiosas deles.

A plataforma utiliza **Inteligência Artificial** para ir além do simples armazenamento, oferecendo busca semântica, respostas a perguntas e automação de processos.

### 🎯 Finalidade e Público-Alvo

**Finalidade:** Transformar arquivos "mortos" (como PDFs digitalizados e documentos físicos) em ativos de dados interativos e pesquisáveis.

**Público-Alvo:**
- 🏢 Grandes empresas (jurídico, financeiro, RH)
- 🏛️ Prefeituras e órgãos governamentais

**Problema Resolvido:**
- ❌ Caos documental
- ❌ Dificuldade em encontrar informações
- ❌ Processos manuais lentos
- ❌ Falta de insights a partir de dados não estruturados

---

## ✨ Funcionalidades Principais

### 📄 Digitalização e OCR
Extração de texto de alta precisão de PDFs (nativos ou de imagem) e documentos digitalizados, página por página.

### 🔍 Busca Semântica (IA)
Permite que os usuários busquem documentos pelo **significado ou contexto**, e não apenas por palavras-chave.

**Exemplo:** *"contratos que vencem nos próximos 90 dias"*

### 💬 Q&A com IA (RAG)
Os usuários podem fazer perguntas diretas e a IA lê os documentos relevantes e fornece uma resposta direta, citando as fontes (documento e página).

**Exemplo:** *"Qual o valor total do contrato X?"*

### 🏢 Gestão Multi-Tenant
Arquitetura segura onde cada empresa cliente tem sua própria organização isolada, com gerenciamento de usuários e papéis (Admin, Editor, Viewer).

### 📦 Armazenamento de Arquivos Escalável
Utiliza uma arquitetura de armazenamento de objetos (compatível com S3) para lidar com milhões de documentos.

### ⚡ Processamento Assíncrono
O upload é instantâneo. O processamento de IA (OCR e geração de embeddings) acontece em segundo plano, garantindo que a plataforma permaneça rápida e responsiva.

---

## 🏛️ Arquitetura do Sistema

\`\`\`
+-----------+       +-------------------------+       +-------------------------+
|           |       |                         |       |                         |
|  Usuário  | ----> |   Frontend (Next.js)    | <---> |   Backend API (FastAPI) |
|           |       | (Interface e Autent.)   |       | (Lógica de Negócio e IA) |
+-----------+       +-------------------------+       +-------------------------+
                                                              |
                          +-----------------------------------+-----------------------------------+
                          |                                   |                                   |
                          v                                   v                                   v
+-------------------------+       +-------------------------+       +-------------------------+
|                         |       |                         |       |                         |
| Banco de Dados (Postgres) |       | Fila de Tarefas (Redis) |       | Armazenamento (S3/MinIO)|
| (Metadados e Vetores)   |       | (Gerencia o processamento)|       | (Arquivos PDF, Imagens) |
+-------------------------+       +-------------------------+       +-------------------------+
                                                |
                                                v
                          +-------------------------+
                          |                         |
                          |  Worker de IA (Celery)  |
                          | (OCR, Embeddings, RAG)  |
                          +-------------------------+
\`\`\`

### 🧩 Componentes

#### **Frontend (intellidocs-saas)**
- **Propósito:** Interface do usuário (UI/UX) com a qual o cliente interage
- **Responsabilidades:** 
  - Renderização de componentes
  - Gerenciamento de estado local
  - Autenticação de usuário (via Firebase)
  - Comunicação com a API Backend

#### **Backend (intellidocs-backend)**
- **Propósito:** O cérebro da aplicação. Expõe uma API RESTful segura
- **Responsabilidades:**
  - Lógica de negócio
  - Validação de tokens de autenticação
  - Gerenciamento de usuários e organizações
  - Orquestração das tarefas de IA

#### **Banco de Dados (PostgreSQL Remoto)**
- **Propósito:** Fonte única da verdade para todos os metadados
- **Responsabilidades:**
  - Armazena informações de usuários, organizações e documentos
  - Vetores de embedding (usando a extensão `pgvector`) para busca semântica

#### **Worker de IA (Celery + Redis)**
- **Propósito:** Lidar com todo o processamento pesado de forma assíncrona
- **Responsabilidades:**
  - Receber tarefas (Ex: "processar documento ID 123")
  - Extrair o texto (OCR)
  - Gerar os embeddings (Hugging Face)
  - Salvar no banco

#### **Armazenamento de Objetos (MinIO/S3)**
- **Propósito:** Armazenamento escalável para os arquivos brutos (PDFs, etc.)
- **Responsabilidades:**
  - Armazenar e servir os arquivos de forma segura
  - Desacoplada da lógica da aplicação

---

## 🚀 Tecnologias Utilizadas

### Frontend (UI)
- **Next.js** - Framework React para renderização (SSR/SSG/CSR)
- **TypeScript** - Tipagem estática para robustez do código
- **Tailwind CSS** - Framework CSS utility-first
- **shadcn/ui** - Componentes de UI modernos e acessíveis
- **Firebase Authentication** - Gerenciamento de login e cadastro

### Backend (API)
- **Python 3.11** - Linguagem principal
- **FastAPI** - Framework web de alta performance para a API
- **SQLAlchemy** - ORM para interação com o PostgreSQL
- **Alembic** - Migrações de esquema do banco de dados
- **Pydantic** - Validação de dados e gerenciamento de configurações

### Inteligência Artificial (IA)
- **Sentence Transformers (Hugging Face)** - Geração de embeddings (vetores) de texto
- **pgvector** - Extensão PostgreSQL para busca vetorial
- **PyPDF2 / pdfplumber** - Extração de texto de PDFs
- **Tesseract OCR** - OCR para documentos digitalizados

### Infraestrutura
- **Docker & Docker Compose** - Containerização
- **Celery** - Processamento assíncrono de tarefas
- **Redis** - Fila de mensagens e cache
- **MinIO / AWS S3** - Armazenamento de objetos

---

## 🛠️ Configuração e Instalação

### Pré-requisitos

- Docker e Docker Compose instalados
- Node.js 18+ e npm/pnpm
- Conta Firebase (para autenticação)
- Banco de dados PostgreSQL remoto (com extensão `pgvector`)

### 1. Configurar Variáveis de Ambiente

#### Backend (.env)

\`\`\`env
# Banco de Dados
DATABASE_URL=postgresql://user:password@host:5432/intellidocs

# Armazenamento
S3_ENDPOINT=http://minio:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET_NAME=intellidocs-files

# Redis
REDIS_URL=redis://redis:6379/0

# Firebase (para validação de tokens)
FIREBASE_PROJECT_ID=seu-projeto-firebase
\`\`\`

#### Frontend (.env.local)

\`\`\`env
# API Backend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Firebase Authentication
NEXT_PUBLIC_FIREBASE_API_KEY=sua-api-key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=seu-projeto.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=seu-projeto-firebase
\`\`\`

### 2. Iniciar o Backend (Docker)

\`\`\`bash
# Clone o repositório do backend
git clone [URL_DO_REPOSITORIO_BACKEND]
cd intellidocs-backend

# Inicie os serviços
docker compose up -d --build

# Execute as migrações do banco de dados
docker compose exec backend alembic upgrade head
\`\`\`

A API estará rodando em `http://localhost:8000`  
Documentação da API: `http://localhost:8000/docs`

### 3. Configurar o Frontend (Next.js)

\`\`\`bash
# Clone o repositório do frontend
git clone [URL_DO_REPOSITORIO_FRONTEND]
cd intellidocs-saas

# Instale as dependências
npm install
# ou
pnpm install

# Execute o servidor de desenvolvimento
npm run dev
# ou
pnpm dev
\`\`\`

A aplicação estará rodando em `http://localhost:3000`

---

## 🔄 Roadmap (Funcionalidades Futuras)

- [ ] **Workflows de Aprovação** - Construtor visual de workflows (Ex: "Documento X precisa ser aprovado por Y e Z")
- [ ] **Classificação Automática** - IA para categorizar e aplicar tags automaticamente no upload
- [ ] **Analytics Avançados** - Dashboards de produtividade, gargalos e uso do sistema
- [ ] **Integração com Assinatura Digital** - Conexão com plataformas de assinatura (DocuSign, etc.)
- [ ] **Relatórios Personalizados com IA** - Geração de relatórios complexos com base em múltiplos documentos

---

## 📝 Licença

Este projeto é proprietário e confidencial. Todos os direitos reservados.

---

## 👥 Contribuindo

Para contribuir com o projeto, entre em contato com a equipe de desenvolvimento.

---

## 📧 Contato

Para mais informações, entre em contato através de [seu-email@exemplo.com]

---

<div align="center">

**Desenvolvido com ❤️ pela equipe IntelliDocs**

</div>
