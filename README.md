# Local RAG AI Assistant

A fully offline AI-powered Q&A assistant built with Microsoft Foundry Local and the RAG (Retrieval-Augmented Generation) pattern.

## What it does
Ask questions about your local documents and get accurate, source-grounded answers — no internet required.

<img width="813" height="685" alt="Screenshot 2026-07-13 145042" src="https://github.com/user-attachments/assets/851dd8ee-3701-4f83-95d7-b5ced71b0966" />

## Tech Stack
- **Microsoft Foundry Local** — on-device LLM inference
- **sentence-transformers** — document embeddings
- **SQLite** — local vector database
- **Streamlit** — web interface
- **Python 3.11**

## Setup

### 1. Install dependencies
pip install -r requirements.txt

### 2. Install & start Foundry Local
Download from: https://aka.ms/foundry-local
Then load a model:
foundry model load phi-3.5-mini

### 3. Add your documents
Put PDF or TXT files in the `documents/` folder.

### 4. Ingest documents
python ingest.py

### 5. Run the app
streamlit run app.py

## Project Structure
- `app.py` — Streamlit web interface
- `main.py` — CLI interface
- `ingest.py` — document ingestion pipeline
- `retriever.py` — vector similarity search
- `llm_client.py` — Foundry Local LLM integration
- `database.py` — SQLite operations

## How it works
1. Documents are split into chunks and embedded using sentence-transformers
2. Embeddings are stored in a local SQLite database
3. User questions are embedded and compared against stored vectors
4. Top matching chunks are retrieved and sent to the local LLM
5. LLM generates an answer grounded in the retrieved context

## Additional
Part of a summer AI program focused on local AI development.
