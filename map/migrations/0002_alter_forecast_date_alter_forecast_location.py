# Generated by Django 4.1.1 on 2023-01-03 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='date',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='location',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
