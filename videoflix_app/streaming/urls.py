from django.urls import path
from .views import ProcessVideoView, grouped_videos, video_detail, upload_video, video_by_token

urlpatterns = [
    path('api/grouped-videos/', grouped_videos, name='grouped_videos'),
    path('<int:id>/', video_detail, name='video_detail'),
    path('upload/', upload_video, name='upload_video'),
    path('process-video/', ProcessVideoView.as_view(), name='process_video'),
    path('video/<str:token>/', video_by_token, name='video_by_token'),
]
