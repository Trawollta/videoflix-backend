from django import forms
from .models import Video, Category

class VideoForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)

    class Meta:
        model = Video
        fields = ['title', 'description', 'cover_file', 'video_file_1080p', 'video_file_720p', 'video_file_480p', 'genre', 'category']
