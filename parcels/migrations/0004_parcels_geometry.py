# Generated by Django 5.0.3 on 2024-04-29 20:26

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("parcels", "0003_remove_parcels_address_remove_parcels_area_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="parcels",
            name="geometry",
            field=django.contrib.gis.db.models.fields.PolygonField(
                null=True, srid=4326
            ),
        ),
    ]
