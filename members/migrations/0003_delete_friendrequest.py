# Generated by Django 4.2.5 on 2023-11-13 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_friendrequest_is_read'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FriendRequest',
        ),
    ]
