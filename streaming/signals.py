import os
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq
from .models import Video
from .tasks import convert_video, convert_video_720p, convert_video_1080p, extract_thumbnail, convert_video_delete
from django.core.cache import cache

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default')
        if instance.video_file_480p:
            queue.enqueue(convert_video, instance.video_file_480p.path)
        if instance.video_file_720p:
            queue.enqueue(convert_video_720p, instance.video_file_720p.path)
        if instance.video_file_1080p:
            queue.enqueue(convert_video_1080p, instance.video_file_1080p.path)
        if instance.video_file_480p:
            queue.enqueue(extract_thumbnail, instance.video_file_480p.path)
    cache.delete_many(keys=cache.keys('*videoList*,*video_detail*'))
            

@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    for video_file in [instance.video_file_480p, instance.video_file_720p, instance.video_file_1080p]:
        if video_file and os.path.isfile(video_file.path):
            os.remove(video_file.path)
            convert_video_delete(video_file.path)
    cache.delete_many(keys=cache.keys('*videoList*,*video_detail*'))
