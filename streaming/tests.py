import os
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Video, Category
from .tasks import convert_video, extract_thumbnail
from user.models import CustomUser as User

class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Action")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Action")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Action")

class VideoModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Drama")
        self.video = Video.objects.create(
            title="Test Video",
            description="This is a test video.",
            genre="Drama",
            category=self.category
        )

    def test_video_creation(self):
        self.assertEqual(self.video.title, "Test Video")
        self.assertEqual(self.video.description, "This is a test video.")
        self.assertEqual(self.video.genre, "Drama")
        self.assertEqual(self.video.category, self.category)

    def test_video_str(self):
        self.assertEqual(str(self.video), "Test Video")

    def test_video_upload(self):
        video_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
        video = Video.objects.create(
            title="Upload Video",
            description="Testing video upload.",
            genre="Documentary",
            category=self.category,
            video_file_480p=video_file
        )
        self.assertTrue(video.video_file_480p)

class VideoProcessingTest(TestCase):

   def convert_video(input_path):
    output_path = input_path.replace('.mp4', '_480p.mp4')
    print(f"Konvertiere {input_path} nach {output_path}")
    
    with open(output_path, 'wb') as f:
        f.write(b"dummy content")
    
    if os.path.exists(output_path):
        print(f"Die Datei {output_path} wurde erfolgreich erstellt.")
    else:
        print(f"Die Datei {output_path} wurde NICHT erstellt.")


   def extract_thumbnail(video_path):
    output_thumbnail = video_path.replace('.mp4', '.jpg')
    # Simulierte Thumbnail-Erstellung
    with open(output_thumbnail, 'wb') as f:
        f.write(b"dummy thumbnail content")
    print(f"Thumbnail erstellt: {output_thumbnail}")


class VideoViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Comedy")
        self.video = Video.objects.create(
            title="Test Video View",
            description="Testing video view.",
            genre="Comedy",
            category=self.category
        )

        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.client.login(email='testuser@example.com', password='testpassword')

    def test_grouped_videos_view(self):
        url = reverse('grouped_videos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_video_detail_view(self):
        url = reverse('video_detail', args=[self.video.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.video.title)


