# AI Log & Document Intelligence

An AI-powered system for document analysis using **Retrieval-Augmented Generation (RAG)**.

**Live Demo:** https://ai-log-document-intelligence2.onrender.com

---

## What It Does

Upload any PDF, TXT, or LOG file and ask natural language questions about it. The system extracts text, chunks it intelligently, generates semantic embeddings, stores them in a FAISS vector database, and retrieves the most relevant context to answer your query.

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
| Deployment | Render |

## Syllabus Topics Covered (CSE3232)

- **LLMs & Embeddings** — SentenceTransformers for semantic vector generation (Lab 6)
- **Vector Databases** — FAISS for similarity search and storage (Lab 7)
- **RAG** — context-aware document Q&A pipeline (Lab 8)
- **Docker** — containerized backend deployment (Lab 11)

## Sample Questions That Work Well

Once a document is uploaded and embedded, try questions like:

- "What is the course name and course code?"
- "Who are the course instructors?"
- "What topics are covered in the syllabus?"
- "What are the assessment criteria?"

Questions that match specific factual content in the document return the best results.

## Known Limitations

**Answer formatting:** Responses may contain extra whitespace and line breaks. This is because PyPDF extracts text directly from PDF layout — tables, columns, and structured formatting in the original PDF don't translate cleanly to plain text. The retrieved content is correct, just not perfectly formatted. A post-processing step to clean extracted text is a planned improvement.

**Confidence scores:** All results currently show "low confidence" — this is a display issue with how FAISS L2 distance scores are mapped to confidence labels, not a reflection of retrieval quality. The retrieved chunks are semantically relevant.

**Free tier resets:** The deployed version on Render uses a free instance that resets between sessions. FAISS index data is stored in memory, so you need to re-upload and re-embed your document after the server restarts. This is a infrastructure limitation, not a code issue.

**File types:** Only PDF, TXT, and LOG files are supported. DOCX support is not yet implemented.

## What We Achieved

- Full RAG pipeline working end-to-end: upload → extract → chunk → embed → retrieve → answer
- Smart chunking that handles PDFs and log files differently
- Semantic search using 384-dimensional vector embeddings
- Source filtering — query results can be filtered by filename
- Containerized with Docker and deployed to cloud
- Simple web UI for non-technical demonstration

## Running Locally

```bash
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```

Visit `http://127.0.0.1:8000` for the UI or `http://127.0.0.1:8000/docs` for API docs.

## Running with Docker

```bash
docker build -t ai-log-intelligence .
docker run -p 8000:8000 ai-log-intelligence
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/upload` | Upload a document (PDF, TXT, LOG) |
| GET | `/extract?file_path=` | Extract text from uploaded file |
| GET | `/chunk?file_path=` | Chunk extracted text |
| GET | `/embed?file_path=` | Generate and store embeddings |
| GET | `/query?question=` | Ask a natural language question |

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
│   ├── static/
│   │   └── index.html
│   └── main.py
├── Dockerfile
├── requirements.txt
└── .gitignore
```

