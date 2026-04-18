# Lecture AI System

An end-to-end AI lecture assistant that turns raw audio into:
- Accurate transcript (Whisper)
- Concise summary (BART)
- Translated summary (Google Translate)
- Context-aware Q&A (FAISS + Sentence Transformers + FLAN-T5)

## Features

- Upload lecture audio from the web UI
- Automatic speech-to-text transcription
- Summarization optimized for long transcripts
- Translation to Indian languages (Hindi, Tamil, Kannada, Telugu)
- Retrieval-Augmented Q&A over lecture content
- Simple REST API with React frontend

## Tech Stack

- Frontend: React, Axios
- Backend: Flask, Flask-CORS
- AI Models:
  - openai-whisper (`base`)
  - `facebook/bart-large-cnn`
  - `sentence-transformers/all-MiniLM-L6-v2`
  - `google/flan-t5-base`
- Vector Search: FAISS

## Project Structure

```text
lecture-ai-system/
  backend/
    app.py
    stt.py
    summarizer.py
    translator.py
    rag.py
    requirements.txt
    uploads/
  frontend/
    src/
    public/
    package.json
  audio/
  uploads/
  README.md
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- Git
- FFmpeg (required by Whisper)

### FFmpeg (Windows)

Install FFmpeg and ensure `ffmpeg.exe` is on PATH.
The backend also checks common Windows install locations automatically.

## Setup Instructions

### 1. Backend setup

```bash
cd backend
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
python app.py
```

Backend runs on: `http://127.0.0.1:5052`

### 2. Frontend setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on: `http://localhost:3000`

## API Endpoints

### `POST /process`

Uploads an audio file, then returns transcript, summary, and translation.

Request:
- Form data
  - `audio`: audio file
  - `lang`: target language code (`hi`, `ta`, `kn`, `te`)

Success response example:

```json
{
  "transcript": "Today we will discuss the basics of machine learning...",
  "summary": "The lecture introduces supervised and unsupervised learning...",
  "translation": "यह व्याख्यान सुपरवाइज्ड और अनसुपरवाइज्ड लर्निंग का परिचय देता है..."
}
```

Error response example:

```json
{
  "error": "Missing audio file in request"
}
```

## Screenshots

The following screenshots show the live UI flow from upload to inference trigger.

### 1. Home Screen

The landing interface presents a research-focused dashboard where users can select an audio file, choose a target language, and run the complete AI pipeline in one click.

![Home Screen](screenshots/01-home.png)

### 2. Audio File Selected

This state confirms the selected lecture file and keeps the processing controls visible, so users can validate input before starting transcription and summarization.

![Audio File Selected](screenshots/02-file-selected.png)

### 3. Processing State

After clicking Process Lecture, the application enters inference mode and begins backend processing (STT, summarization, translation, and retrieval preparation).

![Processing State](screenshots/03-processing.png)

### `POST /ask`

Asks a question against previously processed lecture context.

Request body:

```json
{
  "question": "What are the main types of machine learning?"
}
```

Success response example:

```json
{
  "answer": "The lecture covers supervised, unsupervised, and reinforcement learning."
}
```

## How It Works

1. User uploads lecture audio.
2. Whisper transcribes speech to text.
3. BART summarizes transcript chunks.
4. Summary is translated to selected target language.
5. Transcript is chunked, embedded, and indexed in FAISS.
6. Q&A retrieves top chunks and generates an answer using FLAN-T5.

## Notes

- First run may take longer because models are downloaded.
- For production: use a production WSGI server, persistent storage, and authentication.
- Keep large model caches and generated index files out of Git.

## License

Add your preferred license (MIT/Apache-2.0/etc.) in a `LICENSE` file.
