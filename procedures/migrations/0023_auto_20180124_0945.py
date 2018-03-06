# Generated by Django 2.0 on 2018-01-24 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('procedures', '0022_change_next_people_next_people'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change_next_people',
            name='next_people',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='next_people', to='account.UserProfile', verbose_name='关联下一处理人'),
        ),
    ]