# Generated by Django 2.1 on 2018-10-01 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pycrawl3', '0012_auto_20181001_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogger',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created Time'),
        ),
    ]