import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import os

embedder = SentenceTransformer("all-MiniLM-L6-v2")
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")

INDEX_PATH = "faiss_index.bin"
CHUNKS_PATH = "chunks.txt"

index = None
chunks = []

def build_index(text: str):
    global index, chunks
    words = text.split()
    chunks = [" ".join(words[i:i+200]) for i in range(0, len(words), 200)]
    if not chunks:
        index = None
        return

    embeddings = embedder.encode(chunks).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)
    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        f.write("\n---CHUNK---\n".join(chunks))
    print(f"Saved {index.ntotal} chunks to disk")

def load_index():
    global index, chunks
    if os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
            chunks = f.read().split("\n---CHUNK---\n")
        print(f"Loaded {index.ntotal} chunks from disk")

def answer_question(question: str, top_k: int = 3) -> str:
    if not question or not question.strip():
        return "Please enter a question."

    if index is None:
        load_index()
    if index is None:
        return "Please process a lecture first."

    if not chunks:
        return "Please process a lecture first."

    q_vec = embedder.encode([question]).astype("float32")
    safe_top_k = max(1, min(top_k, index.ntotal))
    _, indices = index.search(q_vec, safe_top_k)
    selected = [chunks[i] for i in indices[0] if 0 <= i < len(chunks) and chunks[i].strip()]
    context = " ".join(selected).strip()

    if not context:
        return "I could not find enough lecture context. Please process a clearer lecture audio file."

    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    try:
        result = qa_pipeline(prompt, max_length=200)
        return result[0]["generated_text"]
    except Exception:
        return "I could not generate an answer for this question. Please try rephrasing it."

load_index()