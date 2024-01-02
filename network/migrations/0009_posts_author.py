# Generated by Django 4.1.4 on 2024-01-02 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_posts_delete_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='author',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
    ]