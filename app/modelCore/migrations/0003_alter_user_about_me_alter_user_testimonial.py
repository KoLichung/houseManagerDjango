# Generated by Django 4.2 on 2023-05-05 23:23

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0002_user_about_me_user_avatar_user_case_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='about_me',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='testimonial',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True),
        ),
    ]
