from django.urls import path
from .views import ParcelList, ParcelFilter, LocateParcelById, LocateParcelByCoordinates

urlpatterns = [
    path('parcels/', ParcelList.as_view()),
    path('parcels/filter', ParcelFilter.as_view()),
    path('parcels/locate/<int:id>', LocateParcelById.as_view()), #TODO should be getting from URL
    path('parcels/locate/point', LocateParcelByCoordinates.as_view()),
]

# parcels/locate
# parcels/id

# Obfuscate