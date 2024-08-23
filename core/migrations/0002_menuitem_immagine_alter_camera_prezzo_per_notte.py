# Generated by Django 5.1 on 2024-08-23 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='immagine',
            field=models.ImageField(blank=True, null=True, upload_to='menu/'),
        ),
        migrations.AlterField(
            model_name='camera',
            name='prezzo_per_notte',
            field=models.FloatField(),
        ),
    ]
