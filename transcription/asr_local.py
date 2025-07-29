from faster_whisper import WhisperModel

def transcribe_local(audio_bytes: bytes, language: str = None) -> dict:
    model = WhisperModel("tiny", compute_type="int8")
    segments, _ = model.transcribe(audio_bytes, language=language, word_timestamps=True)

    output = {"text": "", "segments": []}
    for i, seg in enumerate(segments):
        output["segments"].append({
            "id": i,
            "start": seg.start,
            "end": seg.end,
            "text": seg.text,
            "words": [
                {"start": w.start, "end": w.end, "word": w.word}
                for w in seg.words or []
            ]
        })
        output["text"] += seg.text + " "
    return output
