from django.urls import path
from .views import BuildSRTFileView

urlpatterns = [
    path('build_srt_file/', BuildSRTFileView.as_view(), name='build_srt_file')
]
