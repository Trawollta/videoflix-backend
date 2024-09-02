from rest_framework import serializers
from .models import Video, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class VideoSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    video_files = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'cover_file', 'video_file_1080p', 'video_file_720p', 'video_file_480p', 'category', 'uploaded_at', 'video_files']
        
    def get_video_files(self, obj):
        request = self.context.get('request')
        return {
            '480p': request.build_absolute_uri(obj.video_file_480p.url) if obj.video_file_480p else '',
            '720p': request.build_absolute_uri(obj.video_file_720p.url) if obj.video_file_720p else '',
            '1080p': request.build_absolute_uri(obj.video_file_1080p.url) if obj.video_file_1080p else '',
        }
