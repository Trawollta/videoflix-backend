from rest_framework import serializers
from .models import Video, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class VideoSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    video_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'cover_file', 'video_file_1080p', 'video_file_720p', 'video_file_480p', 'category', 'uploaded_at']
        
    
    def get_video_file_url(self, obj):
        request = self.context.get('request')
        video_url = obj.video_file_480p.url if obj.video_file_480p else ''
        return request.build_absolute_uri(video_url) if request else video_url
