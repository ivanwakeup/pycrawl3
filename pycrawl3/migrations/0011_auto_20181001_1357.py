# Generated by Django 2.1 on 2018-10-01 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pycrawl3', '0010_auto_20181001_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogger',
            name='email',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pycrawl3.Email'),
        ),
    ]
