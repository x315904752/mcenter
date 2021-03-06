# Generated by Django 2.0 on 2018-01-23 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procedures', '0017_auto_20180123_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change_deal_info',
            name='change_action',
            field=models.IntegerField(blank=True, null=True, verbose_name='处理结果'),
        ),
        migrations.AlterField(
            model_name='change_deal_info',
            name='change_note',
            field=models.TextField(null=True, verbose_name='处理意见'),
        ),
        migrations.AlterField(
            model_name='change_info',
            name='change_partner',
            field=models.ManyToManyField(default=None, related_name='change_partner', to='account.UserProfile'),
        ),
    ]
