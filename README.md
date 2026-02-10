# ASR Transcriber Django

A Django REST API for audio transcription with automatic fallback from OpenAI Whisper API to a local CPU-friendly ASR engine (`faster-whisper`). This reduces cost and dependency on external services while ensuring continuous transcription capability.

## Quick Start

### Docker (Recommended)

```bash
cp .env.example .env   # edit with your settings
docker compose up --build
```

The API will be available at http://localhost:8000.

### Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/build_srt_file/` | Upload audio file and get transcription with timestamps |
| GET | `/api/health/` | Health check |
| GET | `/swagger/` | Swagger API documentation |

### Example Request

```bash
curl -X POST http://localhost:8000/api/build_srt_file/ \
  -F "audio=@sample.wav"
```

### Example Response

```json
{
  "text": "Hello world",
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 1.5,
      "text": "Hello world",
      "words": [
        {"start": 0.0, "end": 0.5, "word": "Hello"},
        {"start": 0.5, "end": 1.5, "word": "world"}
      ]
    }
  ]
}
```

## Configuration

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
WHISPER_PROVIDER=auto
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SECRET_KEY=change-me-in-production
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for Whisper transcription | — |
| `WHISPER_PROVIDER` | `openai`, `faster-whisper`, or `auto` | `auto` |
| `DEBUG` | Enable Django debug mode | `False` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `localhost,127.0.0.1` |
| `DJANGO_SECRET_KEY` | Django secret key (required in production) | insecure default |

### Transcription Providers

- **`openai`** — Use OpenAI Whisper API only.
- **`faster-whisper`** — Use local faster-whisper transcription only.
- **`auto`** — Use OpenAI first, fallback to faster-whisper on failure.

## Tech Stack

- **Django 4.2+** / **Django REST Framework** — Web framework and API
- **faster-whisper** — Local Whisper inference (CPU-optimized, int8)
- **OpenAI SDK** — Remote Whisper API
- **Gunicorn** — Production WSGI server
- **WhiteNoise** — Static file serving
- **drf-yasg** — Swagger/OpenAPI documentation
- **Docker** — Containerization with multi-stage build
