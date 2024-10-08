# Generated by Django 5.0.7 on 2024-08-04 18:30

import uuid
from django.db import migrations, models

def generate_unique_tokens(apps, schema_editor):
    CustomUser = apps.get_model('user', 'CustomUser')
    for user in CustomUser.objects.all():
        user.confirmation_token = uuid.uuid4()
        user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='confirmation_token',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(generate_unique_tokens),
    ]
