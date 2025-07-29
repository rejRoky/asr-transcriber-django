import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def transcribe_openai(audio_bytes: bytes) -> dict:
    audio_file = ("temp.wav", audio_bytes)
    response = openai.Audio.transcribe("whisper-1", file=audio_file, response_format="verbose_json")
    return response
