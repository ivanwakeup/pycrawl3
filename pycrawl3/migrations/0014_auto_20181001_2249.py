# Generated by Django 2.1 on 2018-10-01 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pycrawl3', '0013_auto_20181001_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogger',
            name='created_time',
            field=models.DateTimeField(null=True, verbose_name='Created Time'),
        ),
        migrations.AlterField(
            model_name='blogger',
            name='modified_time',
            field=models.DateTimeField(null=True, verbose_name='Modified Time'),
        ),
        migrations.AlterField(
            model_name='email',
            name='created_time',
            field=models.DateTimeField(null=True, verbose_name='Created Time'),
        ),
        migrations.AlterField(
            model_name='email',
            name='modified_time',
            field=models.DateTimeField(null=True, verbose_name='Modified Time'),
        ),
    ]
