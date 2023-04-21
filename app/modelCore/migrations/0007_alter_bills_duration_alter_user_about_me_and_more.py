# Generated by Django 4.2 on 2023-04-20 01:28

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0006_housecase_case_link_user_about_me_user_avatar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bills',
            name='duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='about_me',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='testimonial',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
    ]