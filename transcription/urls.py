from django.urls import path
from .views import BuildSRTFileView, HealthCheckView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health_check'),
    path('build_srt_file/', BuildSRTFileView.as_view(), name='build_srt_file'),
]
