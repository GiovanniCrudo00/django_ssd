# Generated by Django 5.0 on 2023-12-12 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0006_alter_record_humidity_alter_record_wind'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='created_at',
        ),
    ]
