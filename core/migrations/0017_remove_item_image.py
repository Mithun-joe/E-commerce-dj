# Generated by Django 2.2.10 on 2020-04-24 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_item_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image',
        ),
    ]
