import os
import re
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse, HttpResponseForbidden, StreamingHttpResponse, Http404
from .models import Video, Category
from .forms import VideoForm
from .serializer import VideoSerializer, CategorySerializer
import ffmpeg
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response

CACHE_TTL = getattr(settings, 'CACHE_TTL', 300)

class VideoItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    def get_queryset(self):
        queryset = cache.get('videoList')
        if not queryset:
            queryset = Video.objects.all()
            cache.set('videoList', queryset, CACHE_TTL)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

class ProcessVideoView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            input_file = video.video_file_480p.path  # Beispielhafte Eingabedatei

            output_file_480p = os.path.join(settings.MEDIA_ROOT, 'videos', f'{video.id}_480p.mp4')
            output_file_720p = os.path.join(settings.MEDIA_ROOT, 'videos', f'{video.id}_720p.mp4')
            output_file_1080p = os.path.join(settings.MEDIA_ROOT, 'videos', f'{video.id}_1080p.mp4')

            # FFmpeg Videoverarbeitung
            ffmpeg.input(input_file).output(output_file_480p, vf='scale=640:360').run()
            ffmpeg.input(input_file).output(output_file_720p, vf='scale=1280:720').run()
            ffmpeg.input(input_file).output(output_file_1080p, vf='scale=1920:1080').run()

            video.video_file_480p = output_file_480p
            video.video_file_720p = output_file_720p
            video.video_file_1080p = output_file_1080p
            video.save()

            return Response({'status': 'Video erfolgreich verarbeitet'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def grouped_videos(request):
    categories = Category.objects.all()
    result = []
    for category in categories:
        videos = Video.objects.filter(category=category)
        category_data = {
            "category": category.name,
            "videos": [
                {
                    "id": video.id,
                    "title": video.title,
                    "description": video.description,
                    "video_files": {
                        "480p": request.build_absolute_uri(video.video_file_480p.url if video.video_file_480p else ''),
                        "720p": request.build_absolute_uri(video.video_file_720p.url if video.video_file_720p else ''),
                        "1080p": request.build_absolute_uri(video.video_file_1080p.url if video.video_file_1080p else '')
                    },
                    "cover_file": request.build_absolute_uri(video.cover_file.url if video.cover_file else '')
                }
                for video in videos
            ]
        }
        result.append(category_data)
    return JsonResponse(result, safe=False)

def video_detail(request, id):
    cache_key = f'video_detail'
    video_data = cache.get(cache_key)
    if not video_data:
        video = get_object_or_404(Video, id=id)
        video_data = {
            "id": video.id,
            "title": video.title,
            "description": video.description,
            "video_files": {
                "480p": request.build_absolute_uri(video.video_file_480p.url if video.video_file_480p else ''),
                "720p": request.build_absolute_uri(video.video_file_720p.url if video.video_file_720p else ''),
                "1080p": request.build_absolute_uri(video.video_file_1080p.url if video.video_file_1080p else '')
            },
            "category": video.category.name
        }
        cache.set(cache_key, video_data, CACHE_TTL)
    return JsonResponse(video_data)

def upload_video(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Nur Superuser dürfen Videos hochladen.")
    
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('video_list')
    else:
        form = VideoForm()
    return render(request, 'streaming/upload.html', {'form': form})

def video_by_token(request, token):
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    video = get_object_or_404(Video, access_token=token)
    try:
        video_file_path = video.video_file_480p.path if 'iphone' in user_agent or 'ipad' in user_agent or ('safari' in user_agent and not 'chrome' in user_agent) else video.video_file_1080p.path 
        print(video_file_path)
        
        def stream_video(video_path, start=None, end=None):
            with open(video_path, 'rb') as video_file:
                if start:
                    video_file.seek(start)
                while True:
                    bytes_to_read = min(8192, end - video_file.tell() + 1) if end else 8192
                    chunk = video_file.read(bytes_to_read)
                    if not chunk:
                        break
                    yield chunk

        range_header = request.META.get('HTTP_RANGE', '').strip()
        range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
        size = os.path.getsize(video_file_path)
        content_type = 'video/mp4'
        if range_match:
            start, end = range_match.groups()
            start = int(start)
            end = int(end) if end else size - 1
            response = StreamingHttpResponse(stream_video(video_file_path, start, end), status=206, content_type=content_type)
            response['Content-Range'] = f'bytes {start}-{end}/{size}'
        else:
            response = StreamingHttpResponse(stream_video(video_file_path), content_type=content_type)
        response['Accept-Ranges'] = 'bytes'
        response['Content-Length'] = str(size if not range_match else end - start + 1)
        response['Content-Disposition'] = 'inline; filename="video.mp4"'
        return response
    except AttributeError:
        raise Http404("Videodatei nicht gefunden.")
