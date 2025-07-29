from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .srt_builder import build_srt_file


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
            400: "Bad request (missing file)",
            500: "Internal server error"
        }
    )
    def post(self, request, *args, **kwargs):
        audio_file = request.FILES.get("audio")
        if not audio_file:
            return Response({"error": "No audio file provided"}, status=400)
        try:
            result = build_srt_file(audio_file.read())
            return Response(result, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
