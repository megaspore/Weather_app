# Generated by Django 4.1.1 on 2023-01-06 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0007_alter_forecastpoint_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecastpoly',
            name='active',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]