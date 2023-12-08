# Generated by Django 5.0 on 2023-12-08 11:24

import records.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0005_alter_record_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='humidity',
            field=models.IntegerField(validators=[records.validators.validate_humidity]),
        ),
        migrations.AlterField(
            model_name='record',
            name='wind',
            field=models.IntegerField(validators=[records.validators.validate_wind]),
        ),
    ]
