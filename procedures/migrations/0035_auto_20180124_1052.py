# Generated by Django 2.0 on 2018-01-24 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('procedures', '0034_auto_20180124_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change_next_people',
            name='next_people',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='account.UserProfile', verbose_name='关联处理人'),
        ),
    ]