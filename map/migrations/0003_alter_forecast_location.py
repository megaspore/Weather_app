# Generated by Django 4.1.1 on 2023-01-03 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_alter_forecast_date_alter_forecast_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='location',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
