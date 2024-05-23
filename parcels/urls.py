from django.urls import path
from .views import ParcelFilter, LocateParcelById, LocateParcelByCoordinates

urlpatterns = [
    path('parcels/filter', ParcelFilter.as_view(), name='parcels-filter'),
    path('parcels/locate/<int:id>', LocateParcelById.as_view(), name='locate-parcels-by-id'), #getting id from URL
    path('parcels/locate/coordinates', LocateParcelByCoordinates.as_view(), name='locate-parcels-by-coordinates'),
]
