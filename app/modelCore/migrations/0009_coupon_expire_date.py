# Generated by Django 4.2 on 2023-05-11 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0008_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='expire_date',
            field=models.DateTimeField(null=True),
        ),
    ]
