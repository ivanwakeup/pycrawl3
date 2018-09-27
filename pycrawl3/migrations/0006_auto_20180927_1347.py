# Generated by Django 2.1 on 2018-09-27 13:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pycrawl3', '0005_auto_20180820_2053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='createdAt',
        ),
        migrations.RemoveField(
            model_name='seed',
            name='updatedAt',
        ),
        migrations.AddField(
            model_name='email',
            name='createdTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='email',
            name='modifiedTime',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Modified Time'),
        ),
        migrations.AddField(
            model_name='seed',
            name='crawl_count',
            field=models.IntegerField(default=0, verbose_name='Crawl Count'),
        ),
        migrations.AddField(
            model_name='seed',
            name='createdTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seed',
            name='modifiedTime',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Updated Time'),
        ),
    ]
