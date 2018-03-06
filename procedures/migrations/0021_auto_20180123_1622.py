# Generated by Django 2.0 on 2018-01-23 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('procedures', '0020_auto_20180123_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change_info',
            name='change_back',
            field=models.TextField(blank=True, null=True, verbose_name='回退方案'),
        ),
        migrations.AlterField(
            model_name='change_info',
            name='change_create_people',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='change_create_people', to='account.UserProfile'),
        ),
        migrations.AlterField(
            model_name='change_info',
            name='change_flow',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='procedures.change_flow'),
        ),
        migrations.AlterField(
            model_name='change_info',
            name='change_note',
            field=models.TextField(blank=True, null=True, verbose_name='变更记录'),
        ),
        migrations.AlterField(
            model_name='change_info',
            name='change_partner',
            field=models.ManyToManyField(related_name='change_partner', to='account.UserProfile'),
        ),
        migrations.AlterField(
            model_name='change_info',
            name='change_plan',
            field=models.TextField(blank=True, null=True, verbose_name='变更方案'),
        ),
        migrations.AlterField(
            model_name='change_info',
            name='change_target',
            field=models.TextField(blank=True, null=True, verbose_name='变更目的'),
        ),
        migrations.AlterField(
            model_name='change_info',
            name='change_theme',
            field=models.CharField(max_length=100, null=True, verbose_name='变更主题'),
        ),
        migrations.AlterField(
            model_name='change_info',
            name='change_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='procedures.change_type'),
        ),
        migrations.AlterField(
            model_name='change_info',
            name='change_verify_people',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='change_verify_people', to='account.UserProfile'),
        ),
    ]
