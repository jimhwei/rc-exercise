# Generated by Django 5.0.3 on 2024-05-05 20:55

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parcels', '0006_parcel_address_parcel_area_parcel_area_sf_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcel',
            name='geometry',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326),
        ),
    ]
