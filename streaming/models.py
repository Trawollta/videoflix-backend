from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    cover_file = models.FileField(upload_to='covers', default='covers/default.jpg')
    video_file_1080p = models.FileField(upload_to='videos',default='videos/default.mp4', )
    video_file_720p = models.FileField(upload_to='videos', blank=True, null=True)
    video_file_480p = models.FileField(upload_to='videos', blank=True, null=True)
    genre = models.CharField(max_length=80, default=0)
    uploaded_at = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, related_name='videos', on_delete=models.CASCADE)

    def __str__(self):
        return self.title