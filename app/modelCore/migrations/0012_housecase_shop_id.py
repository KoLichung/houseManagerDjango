# Generated by Django 4.2 on 2023-04-26 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0011_housecase_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='housecase',
            name='shop_id',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]