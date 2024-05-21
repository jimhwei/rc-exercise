from django.urls import path
from .views import ParcelFilter, LocateParcelById, LocateParcelByCoordinates

urlpatterns = [
    path('parcels/filter', ParcelFilter.as_view(), name='parcels-filter'),
    path('parcels/locate/<int:id>', LocateParcelById.as_view()), #getting id from URL
    path('parcels/locate/point', LocateParcelByCoordinates.as_view()),
]

# parcels/locate
# parcels/id

# Obfuscate