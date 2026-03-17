# AI Log & Document Intelligence

An AI-powered backend system for intelligent document and log analysis using **Retrieval-Augmented Generation (RAG)**.

## What It Does

Upload any PDF, TXT, or LOG file and ask natural language questions about it. The system extracts text, chunks it intelligently, generates semantic embeddings, stores them in a vector database, and retrieves the most relevant context to answer your query.

## Architecture

```
Upload → Extract → Chunk → Embed → FAISS Store
                                        ↓
                          Query → Retrieve → Answer
```

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2) |
| Vector Store | FAISS |
| Text Extraction | PyPDF |
| Containerization | Docker |

## Syllabus Topics Covered

- **LLMs & Embeddings** — SentenceTransformers for semantic vector generation
- **Vector Databases** — FAISS for similarity search and storage
- **RAG (Retrieval-Augmented Generation)** — context-aware document Q&A
- **DevOps / Docker** — containerized backend deployment

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/upload` | Upload a document (PDF, TXT, LOG) |
| GET | `/extract?file_path=` | Extract text from uploaded file |
| GET | `/chunk?file_path=` | Chunk extracted text |
| GET | `/embed?file_path=` | Generate and store embeddings |
| GET | `/query?question=` | Ask a natural language question |

### Query Parameters for `/query`

- `question` — your natural language question
- `k` — number of chunks to retrieve (default: 5)
- `source` — filter results by filename (optional)

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python -m uvicorn backend.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Running with Docker

```bash
# Build the image
docker build -t ai-log-intelligence .

# Run the container
docker run -p 8000:8000 ai-log-intelligence
```

## Example Usage

**1. Upload a document**
```
POST /upload
Body: form-data, file = yourfile.pdf
```

**2. Embed the document**
```
GET /embed?file_path=uploaded_files/yourfile.pdf
```

**3. Ask a question**
```
GET /query?question=What is this document about?
```

**Response:**
```json
{
  "question": "What is this document about?",
  "answer": "Based on the document context: ...",
  "retrieved_chunks": [...],
  "chunks_returned": 3
}
```

## Project Structure

```
ai-log-document-intelligence/
├── backend/
│   ├── routes/
│   │   ├── upload.py
│   │   ├── extract.py
│   │   ├── chunk.py
│   │   └── embed.py
│   ├── services/
│   │   ├── text_extraction.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   └── file_ingestion.py
│   ├── vector_store/
│   │   └── faiss_store.py
│   └── main.py
├── Dockerfile
├── requirements.txt
└── .gitignore
```
