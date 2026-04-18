import { useState } from "react";
import "./App.css";
import axios from "axios";

const API = "http://localhost:5052";
const LANG_OPTIONS = [
  { value: "hi", label: "Hindi" },
  { value: "ta", label: "Tamil" },
  { value: "kn", label: "Kannada" },
  { value: "te", label: "Telugu" },
];

export default function App() {
  const [file, setFile]         = useState(null);
  const [lang, setLang]         = useState("hi");
  const [result, setResult]     = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer]     = useState("");
  const [loading, setLoading]   = useState(false);
  const [asking, setAsking]     = useState(false);
  const [error, setError]       = useState("");

  const pageBackgroundStyle = {
    backgroundImage: `linear-gradient(120deg, rgba(7, 13, 16, 0.82) 0%, rgba(12, 20, 24, 0.76) 42%, rgba(16, 25, 29, 0.66) 100%), url(${process.env.PUBLIC_URL}/hero-academic-4k.jpg)`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    backgroundAttachment: "fixed",
  };

  const processLecture = async () => {
    if (!file) {
      setError("Please select an audio file before processing.");
      return;
    }

    setError("");
    setAnswer("");
    setLoading(true);
    try {
      const form = new FormData();
      form.append("audio", file);
      form.append("lang", lang);
      const res = await axios.post(`${API}/process`, form);
      setResult(res.data);
    } catch(err) {
      const backendError = err?.response?.data?.error;
      setError(backendError || err.message || "Failed to process lecture.");
      setResult(null);
    }
    setLoading(false);
  };

  const askQuestion = async () => {
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setError("");
    setAsking(true);
    try {
      const res = await axios.post(`${API}/ask`, { question });
      setAnswer(res.data.answer);
    } catch (err) {
      const backendError = err?.response?.data?.error;
      setError(backendError || err.message || "Failed to fetch answer.");
    }
    setAsking(false);
  };

  return (
    <div className="page-shell" style={pageBackgroundStyle}>
      <div className="ambient ambient-left" aria-hidden="true" />
      <div className="ambient ambient-right" aria-hidden="true" />

      <main className="app-frame">
        <header className="hero">
          <p className="eyebrow">Research-Grade Lecture Intelligence</p>
          <h1>Academic AI Lecture Research Tool</h1>
          <p className="subhead">
            Refined transcription, summary, translation, and contextual Q&A for modern academic workflows.
          </p>
        </header>

        <section className="panel controls-panel">
          <div className="controls-grid">
            <label className="control">
              <span className="control-label">Audio File</span>
              <input
                className="control-input"
                type="file"
                accept="audio/*"
                onChange={(e) => setFile(e.target.files[0])}
              />
            </label>

            <label className="control">
              <span className="control-label">Target Language</span>
              <select
                className="control-input"
                value={lang}
                onChange={(e) => setLang(e.target.value)}
              >
                {LANG_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>

            <button className="action-btn" onClick={processLecture} disabled={loading}>
              {loading ? "Processing Lecture..." : "Process Lecture"}
            </button>
          </div>

          <p className="file-badge">
            {file ? `Selected: ${file.name}` : "No file selected yet"}
          </p>
        </section>

        {error && <p className="error-banner">{error}</p>}

        {result && (
          <section className="results-stack">
            <article className="panel result-panel">
              <h2>Transcript</h2>
              <p>{result.transcript || "No transcript returned."}</p>
            </article>

            <article className="panel result-panel">
              <h2>Summary</h2>
              <p>{result.summary || "No summary returned."}</p>
            </article>

            <article className="panel result-panel">
              <h2>Translation</h2>
              <p>{result.translation || "No translation returned."}</p>
            </article>

            <article className="panel qa-panel">
              <h2>Ask Questions About This Lecture</h2>
              <div className="qa-row">
                <input
                  className="control-input"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Ask anything from the processed lecture"
                />
                <button className="action-btn action-btn-secondary" onClick={askQuestion} disabled={asking}>
                  {asking ? "Thinking..." : "Ask"}
                </button>
              </div>

              {answer && (
                <div className="answer-box">
                  <span className="answer-label">Answer</span>
                  <p>{answer}</p>
                </div>
              )}
            </article>
          </section>
        )}
      </main>
    </div>
  );
}
