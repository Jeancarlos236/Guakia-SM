# Generated by Django 5.0.3 on 2024-03-26 02:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_alter_post_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trend',
            old_name='occurences',
            new_name='occurrences',
        ),
    ]
