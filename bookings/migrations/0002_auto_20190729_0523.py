# Generated by Django 2.2.3 on 2019-07-29 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='day',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='day',
            name='lastname',
        ),
    ]