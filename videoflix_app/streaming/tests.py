from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from .tasks import convertVideos
from .models import Category, Video
from django.utils import timezone
from .serializer import VideoSerializer
from rest_framework.test import APIRequestFactory
from unittest.mock import patch, MagicMock
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
import os
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User 



class CategoryModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Action")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Action")
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(str(self.category), self.category.name)

class VideoModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Drama")
        self.video = Video.objects.create(
            title="Testvideo",
            description="Beschreibung des Testvideos",
            cover_file="covers/test.jpg",
            video_file_1080p="videos/test_1080p.mp4",
            video_file_720p="videos/test_720p.mp4",
            video_file_480p="videos/test_480p.mp4",
            genre="Drama",
            uploaded_at=timezone.now(),
            category=self.category
        )

    def test_video_creation(self):
        self.assertEqual(self.video.title, "Testvideo")
        self.assertEqual(self.video.description, "Beschreibung des Testvideos")
        self.assertEqual(self.video.cover_file, "covers/test.jpg")
        self.assertEqual(self.video.video_file_1080p, "videos/test_1080p.mp4")
        self.assertEqual(self.video.video_file_720p, "videos/test_720p.mp4")
        self.assertEqual(self.video.video_file_480p, "videos/test_480p.mp4")
        self.assertEqual(self.video.genre, "Drama")
        self.assertEqual(self.video.category, self.category)
        self.assertTrue(isinstance(self.video, Video))
        self.assertEqual(str(self.video), self.video.title)

class VideoSerializerTests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Drama")
        self.video = Video.objects.create(
            title="Testvideo",
            description="Beschreibung des Testvideos",
            cover_file="covers/test.jpg",
            video_file_1080p="videos/test_1080p.mp4",
            video_file_720p="videos/test_720p.mp4",
            video_file_480p="videos/test_480p.mp4",
            genre="Drama",
            uploaded_at=timezone.now(),
            category=self.category
        )
        factory = APIRequestFactory()
        request = factory.get('/')
        self.serializer = VideoSerializer(instance=self.video, context={'request': request})

    def test_video_serializer_contains_expected_fields(self):

        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'title', 'description', 'cover_file', 'video_file_1080p', 'video_file_720p', 'video_file_480p', 'category', 'uploaded_at', 'video_files'})

class VideoSignalTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Drama")
        self.video = Video.objects.create(
            title="Testvideo",
            description="Beschreibung des Testvideos",
            cover_file=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            video_file_1080p=SimpleUploadedFile(name='test_video_1080p.mp4', content=b'', content_type='video/mp4'),
            video_file_720p=SimpleUploadedFile(name='test_video_720p.mp4', content=b'', content_type='video/mp4'),
            video_file_480p=SimpleUploadedFile(name='test_video_480p.mp4', content=b'', content_type='video/mp4'),
            genre="Drama",
            category=self.category
        )

    @patch('django_rq.get_queue')
    def test_auto_convert_file_on_save(self, mock_get_queue):
        mock_queue = MagicMock()
        mock_get_queue.return_value = mock_queue

        new_video = Video.objects.create(
            title="Neues Testvideo",
            description="Beschreibung des neuen Testvideos",
            cover_file=SimpleUploadedFile(name='new_test_image.jpg', content=b'', content_type='image/jpeg'),
            video_file_1080p=SimpleUploadedFile(name='new_test_video_1080p.mp4', content=b'', content_type='video/mp4'),
            category=self.category
        )

        
        mock_queue.enqueue.assert_called_once_with(convertVideos, new_video, job_timeout=1200)

        

class VideoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='admin', password='admin123')
        self.user = User.objects.create_user(username='user', password='user123')
        self.category = Category.objects.create(name='Kategorie 1')
        
        self.video = Video.objects.create(
            title='Testvideo',
            description='Beschreibung des Testvideos',
            category=self.category,
            video_file_480p=SimpleUploadedFile('test_480p.mp4', b'test_content', content_type='video/mp4'),
            video_file_720p=SimpleUploadedFile('test_720p.mp4', b'test_content', content_type='video/mp4'),
            video_file_1080p=SimpleUploadedFile('test_1080p.mp4', b'test_content', content_type='video/mp4')
        )

