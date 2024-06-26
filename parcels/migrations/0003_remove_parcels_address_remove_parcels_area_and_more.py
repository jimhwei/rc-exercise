# Generated by Django 5.0.3 on 2024-04-29 19:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("parcels", "0002_parcels_geometry"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="parcels",
            name="address",
        ),
        migrations.RemoveField(
            model_name="parcels",
            name="area",
        ),
        migrations.RemoveField(
            model_name="parcels",
            name="area_sf",
        ),
        migrations.RemoveField(
            model_name="parcels",
            name="building_f",
        ),
        migrations.RemoveField(
            model_name="parcels",
            name="density",
        ),
        migrations.RemoveField(
            model_name="parcels",
            name="geometry",
        ),
        migrations.RemoveField(
            model_name="parcels",
            name="gfa_sf",
        ),
        migrations.RemoveField(
            model_name="parcels",
            name="height_m",
        ),
        migrations.RemoveField(
            model_name="parcels",
            name="price",
        ),
        migrations.RemoveField(
            model_name="parcels",
            name="sold_per",
        ),
        migrations.RemoveField(
            model_name="parcels",
            name="storey",
        ),
        migrations.RemoveField(
            model_name="parcels",
            name="type",
        ),
        migrations.RemoveField(
            model_name="parcels",
            name="units",
        ),
        migrations.AlterField(
            model_name="parcels",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
