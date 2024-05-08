from django.urls import path
from .views import ParcelList, LocateParcelById, LocateParcelByCoordinates

urlpatterns = [
    path('parcels/', ParcelList.as_view()),
    path('LocateParcelsById/', LocateParcelById.as_view()),
    path('LocateParcelsByCoordinates/', LocateParcelByCoordinates.as_view()),
]