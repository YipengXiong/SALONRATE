# Generated by Django 2.1.5 on 2022-03-03 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salonrate', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salon',
            name='close_time',
        ),
        migrations.AlterField(
            model_name='salon',
            name='open_time',
            field=models.CharField(default='10:00am-5:00pm', max_length=32),
        ),
    ]
