# Generated by Django 5.0.7 on 2024-08-17 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0006_alter_video_video_file_1080p'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='cover_file',
            field=models.FileField(default='covers/default.jpg', upload_to='covers'),
        ),
    ]
