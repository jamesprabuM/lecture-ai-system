# Run this once to create all project files

open('summarizer.py', 'w').write("""from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str, max_length=200) -> str:
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summaries = []
    for chunk in chunks:
        result = summarizer(chunk, max_length=max_length, min_length=50, do_sample=False)
        summaries.append(result[0]["summary_text"])
    return " ".join(summaries)
""")
print("summarizer.py OK")

open('translator.py', 'w').write("""from googletrans import Translator

translator = Translator()

def translate_text(text: str, target_lang: str = "hi") -> str:
    result = translator.translate(text, dest=target_lang)
    return result.text
""")
print("translator.py OK")

open('rag.py', 'w').write("""import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline

embedder = SentenceTransformer("all-MiniLM-L6-v2")
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")

index = None
chunks = []

def build_index(text: str):
    global index, chunks
    words = text.split()
    chunks = [" ".join(words[i:i+200]) for i in range(0, len(words), 200)]
    embeddings = embedder.encode(chunks).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

def answer_question(question: str, top_k: int = 3) -> str:
    if index is None:
        return "Please process a lecture first."
    q_vec = embedder.encode([question]).astype("float32")
    _, indices = index.search(q_vec, top_k)
    context = " ".join([chunks[i] for i in indices[0]])
    prompt = f"Context: {context}\\n\\nQuestion: {question}\\nAnswer:"
    result = qa_pipeline(prompt, max_length=200)
    return result[0]["generated_text"]
""")
print("rag.py OK")

open('app.py', 'w').write("""from flask import Flask, request, jsonify
from flask_cors import CORS
from stt import transcribe_audio
from summarizer import summarize_text
from translator import translate_text
from rag import build_index, answer_question
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/process", methods=["POST"])
def process_lecture():
    file = request.files["audio"]
    lang = request.form.get("lang", "hi")
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    transcript = transcribe_audio(path)
    summary = summarize_text(transcript)
    translation = translate_text(summary, lang)
    build_index(transcript)
    return jsonify({"transcript": transcript, "summary": summary, "translation": translation})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    answer = answer_question(data["question"])
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
""")
print("app.py OK")

print("\\nAll files created! Run: python app.py")