# SmartDoc-RAG

A local **Retrieval-Augmented Generation (RAG)** application for asking questions about uploaded PDF and DOCX documents.

Built to understand and demonstrate a practical RAG pipeline using **FastAPI, PostgreSQL, pgvector, Ollama, Gemma 3, EmbeddingGemma, and CrossEncoder reranking**.

> No OpenAI API key is required. AI inference runs locally through Ollama.

## Architecture

```text
Document
   ↓
Extract → Clean → Chunk → Embed
   ↓
PostgreSQL + pgvector
   ↓
Question
   ↓
Query Rewriting
   ↓
Vector Retrieval (Top 5)
   ↓
CrossEncoder Reranking (Top 3)
   ↓
Context + Prompt
   ↓
Gemma 3
   ↓
Answer
```

## Key Features

- PDF and DOCX document ingestion
- Text cleaning and overlapping chunking
- 768-dimensional EmbeddingGemma vectors
- PostgreSQL + pgvector semantic search
- Top-5 retrieval with CrossEncoder reranking to Top 3
- Conversation-aware follow-up questions
- Conversation/message persistence
- Duplicate document handling
- Grounded answers with an unknown-answer fallback
- Docker support
- Automated tests

## Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy  
**Database:** PostgreSQL, pgvector, Alembic  
**RAG/AI:** Ollama, Gemma 3 4B, EmbeddingGemma, SentenceTransformers CrossEncoder  
**Frontend:** HTML, CSS, JavaScript  
**Testing:** pytest  
**Deployment:** Docker

## Project Structure

```text
SmartDoc-RAG/
├── app/
│   ├── core/
│   ├── db/
│   ├── etl/
│   ├── rag/
│   └── main.py
├── data/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── README.md
```

## Run Locally

### Prerequisites

- Python 3.13
- Docker Desktop
- Ollama
- Git

### 1. Clone

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd SmartDoc-RAG
```

### 2. Set up Python

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Pull Ollama models

```powershell
ollama pull gemma3:4b
ollama pull embeddinggemma
```

### 4. Configure `.env`

```env
DATABASE_URL=postgresql+psycopg://smartdoc_user:smartdoc_password@localhost:5432/smartdoc_db
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=gemma3:4b
EMBEDDING_MODEL=embeddinggemma
```

### 5. Start the application

```powershell
docker compose up -d --build
```

Open:

**http://localhost:8000**

API documentation:

**http://localhost:8000/docs**

## Usage

1. Upload a PDF or DOCX document.
2. Ask a question about its contents.
3. SmartDoc-RAG retrieves and reranks relevant document chunks.
4. Gemma 3 generates an answer using the retrieved context.

Example:

```text
Question:
How many days of annual leave do employees receive?

Answer:
Employees receive 30 days of annual leave every year.
```

If the information is not available in the documents, the application responds that it could not find the answer.

## Testing

Run:

```powershell
pytest
```

Current test suite:

```text
9 tests passed
```

## Current Status

The complete flow has been validated:

```text
Document Upload
      ↓
ETL & Embeddings
      ↓
Vector Retrieval
      ↓
CrossEncoder Reranking
      ↓
Local LLM
      ↓
Grounded Answer
```

Conversation follow-ups, duplicate uploads, unknown questions, local embeddings, and Docker-based LLM/embedding access have also been tested successfully.

## Future Improvements

- Hybrid keyword + vector search
- Semantic chunking
- Authentication
- More document formats and OCR
- RAG evaluation metrics
- Streaming responses
- Production cloud deployment


                              SMARTDOC-RAG
                         End-to-End RAG Pipeline
                                     
        ┌─────────────────────────────────────────────────────┐
        │                     WEB UI                          │
        │                  HTML / CSS / JS                    │
        └─────────────────────────┬───────────────────────────┘
                                  │
                                  ▼
                        ┌───────────────────┐
                        │      FastAPI      │
                        │      Backend      │
                        └─────────┬─────────┘
                                  │
                 ┌────────────────┴────────────────┐
                 │                                 │
                 │ DOCUMENT INGESTION              │ QUESTION ANSWERING
                 │                                 │
                 ▼                                 ▼
        ┌─────────────────┐              ┌────────────────────┐
        │       ETL       │              │ Conversation       │
        │ Extract         │              │ History            │
        │ Clean           │              └─────────┬──────────┘
        │ Chunk           │                        ▼
        └────────┬────────┘              ┌────────────────────┐
                 ▼                       │ Query Rewriting    │
        ┌─────────────────┐              └─────────┬──────────┘
        │  EmbeddingGemma │                        ▼
        │    768 dims     │              ┌────────────────────┐
        └────────┬────────┘              │ Query Embedding    │
                 │                       └─────────┬──────────┘
                 ▼                                 │
        ┌──────────────────────────────────────────┴───────┐
        │             PostgreSQL + pgvector                │
        │                                                   │
        │  Documents │ Chunks │ Embeddings │ Conversations│
        │                              ▲                    │
        └──────────────────────────────┼────────────────────┘
                                       │
                                       ▼
                              ┌───────────────────┐
                              │ Vector Retrieval  │
                              │      Top 5        │
                              └─────────┬─────────┘
                                        ▼
                              ┌───────────────────┐
                              │   CrossEncoder    │
                              │    Reranking      │
                              │      Top 3        │
                              └─────────┬─────────┘
                                        ▼
                              ┌───────────────────┐
                              │  Context Builder  │
                              └─────────┬─────────┘
                                        ▼
                              ┌───────────────────┐
                              │   Prompt Builder  │
                              └─────────┬─────────┘
                                        ▼
                              ┌───────────────────┐
                              │      Ollama       │
                              │     Gemma 3 4B    │
                              └─────────┬─────────┘
                                        ▼
                              ┌───────────────────┐
                              │  Grounded Answer  │
                              └─────────┬─────────┘
                                        │
                                        ▼
                              ┌───────────────────┐
                              │     Web UI        │
                              └───────────────────┘