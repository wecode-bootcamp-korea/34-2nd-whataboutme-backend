# Generated by Django 4.0.6 on 2022-07-14 07:50

import core.models
import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('motels', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('checkin', models.DateField(default=datetime.datetime(2022, 7, 14, 7, 50, 0, 644618, tzinfo=utc))),
                ('checkout', models.DateField(default=core.models.tomorrow)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservationrooms', to='motels.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservationusers', to='users.user')),
            ],
            options={
                'db_table': 'reservations',
            },
        ),
    ]
