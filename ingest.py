import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from database import init_db, insert_chunk, clear_db

DOCUMENTS_DIR = "documents"
CHUNK_SIZE = 400       # karakter cinsinden
CHUNK_OVERLAP = 80     # chunk'lar arası örtüşme

# Embedding modeli — ilk çalıştırmada indirir, sonra local çalışır
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def chunk_text(text):
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

def ingest_documents():
    init_db()
    clear_db()  # Yeniden yüklemede temizle

    files = os.listdir(DOCUMENTS_DIR)
    if not files:
        print("documents/ klasörü boş! İçine PDF veya TXT dosyası koy.")
        return

    for filename in files:
        path = os.path.join(DOCUMENTS_DIR, filename)

        if filename.endswith(".pdf"):
            text = read_pdf(path)
        elif filename.endswith(".txt") or filename.endswith(".md"):
            text = read_txt(path)
        else:
            print(f"Atlandı (desteklenmiyor): {filename}")
            continue

        chunks = chunk_text(text)
        print(f"{filename} → {len(chunks)} chunk")

        for chunk in chunks:
            embedding = embedding_model.encode(chunk).tolist()
            insert_chunk(source=filename, content=chunk, embedding=embedding)

    print("Tüm belgeler başarıyla yüklendi!")

if __name__ == "__main__":
    ingest_documents()