# Generated by Django 5.0.3 on 2024-05-23 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcels', '0010_alter_parcel_storey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcel',
            name='address',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='area',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='area_sf',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='building_f',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='density',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='gfa_sf',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='height_m',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='parcel_type',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='proj_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='sold_per',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='status',
            field=models.CharField(default=0, max_length=255),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='units',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
