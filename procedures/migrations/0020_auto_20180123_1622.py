# Generated by Django 2.0 on 2018-01-23 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procedures', '0019_change_info_change_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change_info',
            name='change_flag',
            field=models.IntegerField(verbose_name='变更状态'),
        ),
    ]
