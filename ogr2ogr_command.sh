> ogr2ogr -f "PostgreSQL" PG:"dbname=postgres user=postgres password=postgres" "/Users/jimwei/Projects/RC Django API Exercise/toronto.geojson" -nln public.parcels_parcel -append

# INSERT INTO "parcels_parcel" ("geometry" , "id", "proj_name", "status", "address", "area", "area_sf", "building_f", "density", "gfa_sf", "height_m", "price", "sold_per", "storey", "type", "units") VALUES ('0106000020E6100000010000000103000000010000000500000046A408F7A7D953C0C997311708D3454028D6B64199D953C0C47748080ED345404300E41697D953C005C76CA901D34540E78692A0A5D953C0ECB97686FBD2454046A408F7A7D953C0C997311708D34540'::GEOMETRY, '1', 'Garden Tower', 'Under Construction', '15 Denison Avenue', 3271.17, 35210.55, 24647.39, 28, 985895.6, 140, 823711.7, 100, 40, 'Commercial', 986)