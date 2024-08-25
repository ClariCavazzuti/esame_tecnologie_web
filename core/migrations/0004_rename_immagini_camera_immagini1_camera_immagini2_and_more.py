# Generated by Django 5.1 on 2024-08-25 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_core'),
    ]

    operations = [
        migrations.RenameField(
            model_name='camera',
            old_name='immagini',
            new_name='immagini1',
        ),
        migrations.AddField(
            model_name='camera',
            name='immagini2',
            field=models.ImageField(blank=True, null=True, upload_to='camere/'),
        ),
        migrations.AddField(
            model_name='camera',
            name='immagini3',
            field=models.ImageField(blank=True, null=True, upload_to='camere/'),
        ),
    ]
