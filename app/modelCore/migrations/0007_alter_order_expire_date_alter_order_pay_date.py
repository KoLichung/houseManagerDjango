# Generated by Django 4.2 on 2023-05-09 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0006_alter_user_video_bg_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='expire_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='pay_date',
            field=models.DateTimeField(null=True),
        ),
    ]
