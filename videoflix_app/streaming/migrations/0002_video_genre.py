# Generated by Django 5.0.7 on 2024-07-30 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='genre',
            field=models.CharField(default=0, max_length=80),
        ),
    ]
