# Generated by Django 4.1.1 on 2023-01-03 20:10

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_alter_forecast_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForecastPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(blank=True, max_length=10)),
                ('location', models.CharField(blank=True, max_length=500)),
                ('active', models.BooleanField()),
                ('temp_max_forecast', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('temp_min_forecast', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('temp_max_observation', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('temp_min_observation', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('bias_temp_max', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('bias_temp_min', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('to_date_rmse_temp_max', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('to_date_rmse_temp_min', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('_7_days_rmse_temp_max', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('_7_days_rmse_temp_min', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('_30_days_rmse_temp_max', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('_30_days_rmse_temp_min', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='ForecastPoly',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(blank=True, max_length=10)),
                ('location', models.CharField(blank=True, max_length=500)),
                ('active', models.BooleanField()),
                ('temp_max_forecast', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('temp_min_forecast', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('temp_max_observation', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('temp_min_observation', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('bias_temp_max', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('bias_temp_min', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('to_date_rmse_temp_max', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('to_date_rmse_temp_min', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('_7_days_rmse_temp_max', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('_7_days_rmse_temp_min', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('_30_days_rmse_temp_max', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('_30_days_rmse_temp_min', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('polygon', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326)),
            ],
        ),
        migrations.DeleteModel(
            name='Forecast',
        ),
    ]
