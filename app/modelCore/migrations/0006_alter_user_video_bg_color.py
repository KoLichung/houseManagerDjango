# Generated by Django 4.2 on 2023-05-08 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0005_user_video_bg_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='video_bg_color',
            field=models.CharField(blank=True, default='', max_length=10, null=True),
        ),
    ]
