# Generated by Django 3.2 on 2023-02-01 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_remove_title_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
