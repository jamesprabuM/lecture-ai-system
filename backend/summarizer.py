from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str, max_length=200) -> str:
    if not text or not text.strip():
        return "No speech detected in audio."

    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summaries = []
    for chunk in chunks:
        if not chunk.strip():
            continue
        try:
            # Use adaptive bounds for short chunks to avoid generation shape errors.
            words = len(chunk.split())
            min_len = 20 if words >= 40 else 5
            max_len = max(32, min(max_length, words + 32))
            result = summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)
            summaries.append(result[0]["summary_text"])
        except Exception:
            # Skip malformed/too-short chunks instead of failing the entire request.
            continue
    if not summaries:
        return "No speech detected in audio."
    return " ".join(summaries)