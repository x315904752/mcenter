# Generated by Django 2.0 on 2018-01-23 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procedures', '0016_auto_20180123_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change_deal_info',
            name='change_action',
            field=models.IntegerField(null=True, verbose_name='处理结果'),
        ),
        migrations.AlterField(
            model_name='change_deal_info',
            name='change_note',
            field=models.TextField(blank=True, null=True, verbose_name='处理意见'),
        ),
    ]