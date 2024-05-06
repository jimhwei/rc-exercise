# Generated by Django 5.0.3 on 2024-05-05 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcels', '0005_rename_parcels_parcel'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcel',
            name='address',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parcel',
            name='area',
            field=models.FloatField(default=100.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parcel',
            name='area_sf',
            field=models.FloatField(default=100.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parcel',
            name='building_f',
            field=models.FloatField(default=100.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parcel',
            name='density',
            field=models.FloatField(default=100.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parcel',
            name='gfa_sf',
            field=models.FloatField(default=100.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parcel',
            name='height_m',
            field=models.FloatField(default=100.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parcel',
            name='price',
            field=models.FloatField(default=100.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parcel',
            name='sold_per',
            field=models.FloatField(default=100.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parcel',
            name='storey',
            field=models.PositiveSmallIntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parcel',
            name='type',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parcel',
            name='units',
            field=models.PositiveSmallIntegerField(default=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='parcel',
            name='id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]