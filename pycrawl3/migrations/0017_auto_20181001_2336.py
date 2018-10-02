# Generated by Django 2.1 on 2018-10-01 23:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pycrawl3', '0016_auto_20181001_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='created_time',
            field=models.DateTimeField(verbose_name='Created Time'),
        ),
        migrations.AlterField(
            model_name='email',
            name='modified_time',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now, verbose_name='Modified Time'),
            preserve_default=False,
        ),
    ]
