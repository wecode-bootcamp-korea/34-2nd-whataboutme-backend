# Generated by Django 4.0.6 on 2022-07-11 04:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('motel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='checkin',
            field=models.DateField(default=datetime.datetime(2022, 7, 11, 4, 40, 6, 950282, tzinfo=utc)),
        ),
    ]