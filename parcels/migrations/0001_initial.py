# Generated by Django 5.0.3 on 2024-03-25 15:15

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Parcels",
            fields=[
                (
                    "id",
                    models.CharField(
                        max_length=50, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("proj_name", models.CharField(max_length=255)),
                ("area", models.FloatField()),
                ("status", models.CharField(max_length=255)),
                ("area_sf", models.FloatField()),
                ("building_f", models.FloatField()),
                ("height_m", models.FloatField()),
                ("storey", models.PositiveSmallIntegerField()),
                ("gfa_sf", models.FloatField()),
                ("density", models.FloatField()),
                ("price", models.FloatField()),
                ("units", models.PositiveSmallIntegerField()),
                ("sold_per", models.FloatField()),
                ("type", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
            ],
        ),
    ]
