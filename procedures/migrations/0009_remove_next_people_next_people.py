# Generated by Django 2.0 on 2018-01-19 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('procedures', '0008_auto_20180119_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='next_people',
            name='next_people',
        ),
    ]
