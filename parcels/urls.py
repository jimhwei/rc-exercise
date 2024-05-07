from django.urls import include, path
# from .views import ParcelCreate, ParcelList, ParcelDetail, ParcelUpdate, ParcelDelete
from .views import ParcelList, LocateParcel
# from .views import parcel_list
from parcels import views

urlpatterns = [
    # path('create/', ParcelCreate.as_view(), name='create-Parcel'),
    # path('', ParcelList.as_view()),
    # path('<int:pk>/', ParcelDetail.as_view(), name='retrieve-Parcel'),
    # path('update/<int:pk>/', ParcelUpdate.as_view(), name='update-Parcel'),
    # path('delete/<int:pk>/', ParcelDelete.as_view(), name='delete-Parcel')
    
    path('parcels/', ParcelList.as_view()),
    path('LocateParcels/', LocateParcel.as_view()),

]