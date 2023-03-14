# Generated by Django 3.2 on 2023-02-02 10:02

import reviews.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_remove_title_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(db_index=True, help_text='Укажите год выпуска', validators=[reviews.validators.validate_year], verbose_name='Год издания/публикации произведения'),
        ),
    ]
