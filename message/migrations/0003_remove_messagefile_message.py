# Generated by Django 4.2.4 on 2023-09-01 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0002_message_mid_messagefile_mid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messagefile',
            name='message',
        ),
    ]