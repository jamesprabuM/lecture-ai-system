from googletrans import Translator

translator = Translator()

def translate_text(text: str, target_lang: str = "hi") -> str:
    if not text or not str(text).strip():
        return ""

    try:
        result = translator.translate(text, dest=target_lang)
        translated = getattr(result, "text", None)
        return translated if translated else text
    except Exception:
        # Keep the API stable even when translation provider is unavailable.
        return text