from flask import Flask, request, jsonify
from flask_cors import CORS
from stt import transcribe_audio
from summarizer import summarize_text
from translator import translate_text
from rag import build_index, answer_question
import os
import traceback

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/process", methods=["POST"])
def process_lecture():
    if "audio" not in request.files:
        return jsonify({"error": "Missing audio file in request"}), 400

    file = request.files["audio"]
    if not file or not file.filename:
        return jsonify({"error": "Invalid audio file"}), 400

    lang = request.form.get("lang", "hi")
    path = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        file.save(path)
        transcript = transcribe_audio(path)
        summary = summarize_text(transcript)
        translation = translate_text(summary, lang)
        build_index(transcript)
        return jsonify({"transcript": transcript, "summary": summary, "translation": translation})
    except Exception as exc:
        traceback.print_exc()
        return jsonify({"error": str(exc)}), 500

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}
    question = data.get("question", "")
    answer = answer_question(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    # Use a single-process dev server to avoid multiple reloader instances.
    app.run(debug=False, host="127.0.0.1", port=5052, use_reloader=False)