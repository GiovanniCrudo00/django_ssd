# Generated by Django 5.0 on 2023-12-07 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Records',
            new_name='Record',
        ),
    ]