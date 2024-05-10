SELECT b.*
FROM public.parcels_parcel a, public.parcels_parcel b
WHERE a.id ='1' AND ST_DWithin(a.geometry, b.geometry, 0.001)

-- Finding the SRID
SELECT Find_SRID('public', 'parcels_parcel', 'geometry');

SELECT "parcels_parcel"."id", "parcels_parcel"."proj_name", "parcels_parcel"."area", "parcels_parcel"."status", "parcels_parcel"."area_sf", "parcels_parcel"."building_f", "parcels_parcel"."height_m", "parcels_parcel"."storey", "parcels_parcel"."gfa_sf", "parcels_parcel"."density", "parcels_parcel"."price", "parcels_parcel"."units", "parcels_parcel"."sold_per", "parcels_parcel"."type", "parcels_parcel"."address", "parcels_parcel"."geometry"::bytea FROM "parcels_parcel" WHERE "parcels_parcel"."id" = '1' ORDER BY "parcels_parcel"."id" ASC LIMIT 1; args=('1',); alias=default

(0.004) SELECT "spatial_ref_sys"."srid", "spatial_ref_sys"."auth_name", "spatial_ref_sys"."auth_srid", "spatial_ref_sys"."srtext", "spatial_ref_sys"."proj4text" FROM "spatial_ref_sys" WHERE "spatial_ref_sys"."srid" = 4326 LIMIT 21; args=(4326,); alias=default

(0.043) SELECT "parcels_parcel"."id", "parcels_parcel"."proj_name", "parcels_parcel"."area", "parcels_parcel"."status", "parcels_parcel"."area_sf", "parcels_parcel"."building_f", "parcels_parcel"."height_m", "parcels_parcel"."storey", "parcels_parcel"."gfa_sf", "parcels_parcel"."density", "parcels_parcel"."price", "parcels_parcel"."units", "parcels_parcel"."sold_per", "parcels_parcel"."type", "parcels_parcel"."address", "parcels_parcel"."geometry"::bytea FROM "parcels_parcel" WHERE ST_DistanceSphere("parcels_parcel"."geometry", ST_GeomFromEWKB('\001\001\000\000 \346\020\000\000\272\275\2441Z\331S\300\246\233\304 \260\322E@'::bytea)) <= 10000.0; args=(<django.contrib.gis.db.backends.postgis.adapter.PostGISAdapter object at 0x10c10de80>, 10000.0); alias=default