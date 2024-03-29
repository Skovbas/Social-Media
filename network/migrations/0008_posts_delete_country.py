# Generated by Django 4.1.4 on 2023-12-29 18:26

from django.db import migrations, models
import network.models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('location', models.CharField(max_length=255)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=network.models.get_post_image_filepath)),
            ],
        ),
        migrations.DeleteModel(
            name='Country',
        ),
    ]
