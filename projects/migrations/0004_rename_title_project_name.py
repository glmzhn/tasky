# Generated by Django 4.2.5 on 2023-11-04 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_remove_task_folder_delete_folder_delete_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='title',
            new_name='name',
        ),
    ]
