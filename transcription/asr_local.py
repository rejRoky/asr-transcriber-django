import io
from faster_whisper import WhisperModel

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = WhisperModel("tiny", compute_type="int8")
    return _model


def transcribe_local(audio_bytes: bytes, language: str = None) -> dict:
    model = _get_model()
    segments, _ = model.transcribe(
        io.BytesIO(audio_bytes), language=language, word_timestamps=True
    )

    texts = []
    output_segments = []
    for i, seg in enumerate(segments):
        output_segments.append({
            "id": i,
            "start": seg.start,
            "end": seg.end,
            "text": seg.text,
            "words": [
                {"start": w.start, "end": w.end, "word": w.word}
                for w in seg.words or []
            ]
        })
        texts.append(seg.text)

    return {"text": " ".join(texts), "segments": output_segments}
