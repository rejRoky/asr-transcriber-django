import logging

from django.conf import settings
from .openai_utils import transcribe_openai
from .asr_local import transcribe_local

logger = logging.getLogger(__name__)


def build_srt_file(audio_bytes: bytes, language: str = None) -> dict:
    provider = settings.WHISPER_PROVIDER
    if provider == "openai":
        return transcribe_openai(audio_bytes)
    elif provider == "faster-whisper":
        return transcribe_local(audio_bytes, language)
    elif provider == "auto":
        try:
            return transcribe_openai(audio_bytes)
        except Exception as e:
            logger.warning("OpenAI failed, falling back to local: %s", e)
            return transcribe_local(audio_bytes, language)
