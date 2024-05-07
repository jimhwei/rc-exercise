SELECT b.*
FROM public.parcels_parcel a, public.parcels_parcel b
WHERE a.id ='1' AND ST_DWithin(a.geometry, b.geometry, 0.001)

-- Finding the SRID
SELECT Find_SRID('public', 'parcels_parcel', 'geometry');
