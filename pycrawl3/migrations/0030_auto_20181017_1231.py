# Generated by Django 2.1 on 2018-10-17 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pycrawl3', '0029_potentialblogger'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogger',
            name='found_current_year',
            field=models.BooleanField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='seed',
            name='category',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='potentialblogger',
            name='domain',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Domain'),
        ),
        migrations.AlterField(
            model_name='potentialblogger',
            name='email_address',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Email Address'),
        ),
    ]
