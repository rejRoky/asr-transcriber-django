import logging

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .srt_builder import build_srt_file

logger = logging.getLogger(__name__)

MAX_UPLOAD_SIZE = getattr(settings, "FILE_UPLOAD_MAX_MEMORY_SIZE", 50 * 1024 * 1024)


class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "ok"})


class BuildSRTFileView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Upload audio and get subtitle transcription",
        manual_parameters=[
            openapi.Parameter(
                name="audio",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="Audio file (WAV/MP3/FLAC)",
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Transcription successful",
                examples={
                    "application/json": {
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
                }
            ),
            400: "Bad request (missing file or file too large)",
            500: "Internal server error"
        }
    )
    def post(self, request, *args, **kwargs):
        audio_file = request.FILES.get("audio")
        if not audio_file:
            return Response({"error": "No audio file provided"}, status=400)

        if audio_file.size > MAX_UPLOAD_SIZE:
            limit_mb = MAX_UPLOAD_SIZE // (1024 * 1024)
            return Response(
                {"error": f"File too large. Maximum size is {limit_mb}MB."},
                status=400,
            )

        try:
            result = build_srt_file(audio_file.read())
            return Response(result, status=200)
        except Exception as e:
            logger.exception("Transcription failed")
            return Response({"error": "Transcription failed"}, status=500)
