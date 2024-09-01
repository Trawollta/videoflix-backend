
from .models import Video
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
import django_rq
import os
from .tasks import convertVideos


@receiver(post_save, sender=Video)
def auto_convert_file_on_save(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convertVideos, instance, job_timeout=1200) 
        


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):

    if instance.cover_file:
        cover_file_path = instance.cover_file.path
        if os.path.isfile(cover_file_path):
            os.remove(cover_file_path)

    if instance.video_file_480p:
        video_file_path_480p = instance.video_file_480p.path
        if os.path.isfile(video_file_path_480p):
            os.remove(video_file_path_480p)

    if instance.video_file_720p:
        video_file_path_720p = instance.video_file_720p.path
        if os.path.isfile(video_file_path_720p):
            os.remove(video_file_path_720p)
            
    if instance.video_file_1080p:
        video_file_path_1080p = instance.video_file_1080p.path
        if os.path.isfile(video_file_path_1080p):
            os.remove(video_file_path_1080p)

    if instance.cover_file:
        cover_file_path = instance.cover_file.path
        if os.path.isfile(cover_file_path):
            os.remove(cover_file_path)
