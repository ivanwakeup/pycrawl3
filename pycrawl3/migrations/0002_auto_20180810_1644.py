# Generated by Django 2.1 on 2018-08-10 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pycrawl3', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='email',
            name='createdAt',
            field=models.DateTimeField(auto_now=True, verbose_name='Created Time'),
        ),
    ]