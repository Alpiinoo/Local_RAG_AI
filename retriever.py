import json
import numpy as np
from sentence_transformers import SentenceTransformer
from database import get_all_chunks

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def cosine_similarity(vec1, vec2):
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def get_top_chunks(query, top_k=3):
    query_embedding = embedding_model.encode(query).tolist()
    all_chunks = get_all_chunks()

    scored = []
    for row in all_chunks:
        chunk_id, source, content, embedding_json = row
        chunk_embedding = json.loads(embedding_json)
        score = cosine_similarity(query_embedding, chunk_embedding)
        scored.append((score, source, content))

    # En yüksek skordan küçüğe sırala
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]