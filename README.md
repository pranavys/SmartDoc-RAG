# SmartDoc-RAG

SmartDoc-RAG is an end-to-end Retrieval-Augmented Generation (RAG) project that allows users to ask questions about uploaded documents.

I built this project to understand how a practical RAG application works from the data ingestion stage to generating an answer with a local LLM.

The project focuses on the complete flow:

Document → ETL → Chunking → Embeddings → Vector Database → Retrieval → Reranking → LLM → Answer

## What the project does

SmartDoc-RAG takes documents such as PDF and DOCX files and processes them through an ETL pipeline.

The documents are:

1. Extracted into text
2. Cleaned and transformed
3. Split into smaller chunks
4. Converted into embeddings
5. Stored in PostgreSQL using pgvector

When a user asks a question, the application will:

1. Convert the question into an embedding
2. Search PostgreSQL for similar document chunks
3. Rerank the retrieved results
4. Combine the relevant context with the conversation history
5. Send the final prompt to a local LLM
6. Return the generated answer

## Main Technologies

- Python
- FastAPI
- PostgreSQL
- pgvector
- SQLAlchemy
- Alembic
- LangChain
- Ollama
- Gemma 3
- EmbeddingGemma
- Docker
- HTML/CSS

The project uses Ollama locally, so an OpenAI API key is not required.

## Project Architecture

```text
                    SmartDoc-RAG
                         |
                         v
                  PDF / DOCX Files
                         |
                         v
                      ETL
                 +-------+-------+
                 |               |
              Extract         Transform
                 |               |
                 |          Clean + Chunk
                 |               |
                 +-------+-------+
                         |
                         v
                    Embeddings
                         |
                         v
                   EmbeddingGemma
                         |
                         v
                PostgreSQL + pgvector
                         |
                         |
              ---------------------
              |                   |
           User Query        Chat History
              |                   |
              v                   |
          Embedding               |
              |                   |
              +---------+---------+
                        |
                        v
                Vector Retrieval
                        |
                        v
                    Reranking
                        |
                        v
                 Prompt Building
                        |
                        v
                    Gemma 3
                        |
                        v
                     Answer