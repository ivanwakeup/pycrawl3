# Generated by Django 2.1 on 2018-10-12 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pycrawl3', '0027_auto_20181012_1411'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='new_Blogger',
            new_name='Blogger',
        ),
        migrations.RenameModel(
            old_name='new_Email',
            new_name='Email',
        ),
        migrations.RenameModel(
            old_name='new_Seed',
            new_name='Seed',
        ),
    ]
