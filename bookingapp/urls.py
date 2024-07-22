from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.RoomListView.as_view(), name='all-rooms'),
    path('roomdetails/<int:pk>/', views.RoomDetailView.as_view(), name='room-details'),
    path('bookroom/', views.RoomBookingView.as_view(), name='book-room'),
    path('mybookings/', views.GetBookingView.as_view(), name='my-bookings'),
    path('roomfilter/', views.RoomFilterSortView.as_view(), name='room-filter'),
    path('availabilityrooms/', views.RoomAvailabilityView.as_view(), name='availability-rooms'),
    path('cancelbook/<int:pk>/', views.CancelBookingView.as_view(), name='cancel-book')
]
