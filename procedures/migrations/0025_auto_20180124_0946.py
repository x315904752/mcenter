# Generated by Django 2.0 on 2018-01-24 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('procedures', '0024_auto_20180124_0946'),
    ]

    operations = [
        migrations.RenameField(
            model_name='change_next_people',
            old_name='next_people',
            new_name='next_people_id',
        ),
    ]
