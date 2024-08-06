from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'bookroom', views.RoomBookingView, basename='bookroom')
router.register(
    r'availabilityrooms',
    views.RoomAvailabilityView,
    basename='availabilityrooms'
)
router.register(r'cancelbook', views.CancelBookingView, basename='cancelbook')


urlpatterns = [
    path('rooms/', views.RoomListView.as_view(), name='all-rooms'),
    path(
        'roomdetails/<int:pk>/',
        views.RoomDetailView.as_view(),
        name='room-details'
    ),
    path('mybookings/', views.GetBookingView.as_view(), name='my-bookings'),
    path(
        'roomfilter/',
        views.RoomFilterSortView.as_view(),
        name='room-filter'
    ),
    path('', include(router.urls)),
]
