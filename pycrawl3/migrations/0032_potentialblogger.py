# Generated by Django 2.1 on 2018-10-18 01:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pycrawl3', '0031_auto_20181017_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='PotentialBlogger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_address', models.CharField(max_length=1000, verbose_name='Email Address')),
                ('other_emails', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Other new_Emails')),
                ('domain', models.CharField(max_length=1000, null=True, verbose_name='Domain')),
                ('category', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Category')),
                ('tags', models.CharField(max_length=1000, null=True, verbose_name='Tags')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='Modified Time')),
                ('seed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pycrawl3.Seed')),
            ],
        ),
    ]