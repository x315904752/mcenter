# Generated by Django 2.0 on 2018-01-24 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('procedures', '0026_auto_20180124_0947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='change_next_people',
            name='change_flow',
        ),
    ]
