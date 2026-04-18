import os
import shutil

import whisper

model = whisper.load_model("base")


def _ensure_ffmpeg_available() -> None:
    if shutil.which("ffmpeg") is not None:
        return

    candidate_dirs = [
        os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Microsoft",
            "WinGet",
            "Packages",
            "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe",
            "ffmpeg-8.1-full_build",
            "bin",
        ),
        os.path.join("C:\\", "Program Files", "ffmpeg", "bin"),
    ]

    for candidate_dir in candidate_dirs:
        ffmpeg_path = os.path.join(candidate_dir, "ffmpeg.exe")
        if os.path.exists(ffmpeg_path):
            os.environ["PATH"] = candidate_dir + os.pathsep + os.environ.get("PATH", "")
            return

    raise RuntimeError(
        "ffmpeg is not installed or not on PATH. Install ffmpeg and restart the backend."
    )

def transcribe_audio(file_path: str) -> str:
    _ensure_ffmpeg_available()
    result = model.transcribe(file_path)
    return result["text"]