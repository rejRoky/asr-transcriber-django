# ASR Fallback Feature

This project supports audio transcription with an automatic fallback from OpenAI Whisper API to a local CPU-friendly ASR engine (`faster-whisper`). This reduces cost and dependency on external services while ensuring continuous transcription capability.

---

## Configuration

Set environment variables in your `.env` or system environment:

- `OPENAI_API_KEY` — Your OpenAI API key for Whisper transcription.
- `WHISPER_PROVIDER` — Choose transcription provider:

  - `openai` — Use OpenAI Whisper API only.
  - `faster-whisper` — Use local faster-whisper transcription only.
  - `auto` — Use OpenAI first, fallback to faster-whisper on failure.

Example `.env`:

```bash
OPENAI_API_KEY=your_openai_api_key_here
WHISPER_PROVIDER=auto
```