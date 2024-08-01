from django.test import TestCase
from django.urls import reverse, resolve
from bookingapp import views


class TestUrls(TestCase):
    def test_rooms_url(self):
        url = reverse('all-rooms')
        self.assertEquals(resolve(url).func.view_class, views.RoomListView)

    def test_roomdetails_url(self):
        url = reverse('room-details', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.RoomDetailView)

    def test_bookroom_url(self):
        url = reverse('book-room')
        self.assertEquals(resolve(url).func.view_class, views.RoomBookingView)

    def test_mybookings_url(self):
        url = reverse('my-bookings')
        self.assertEquals(resolve(url).func.view_class, views.GetBookingView)

    def test_roomfilter_url(self):
        url = reverse('room-filter')
        self.assertEquals(
            resolve(url).func.view_class, views.RoomFilterSortView
        )

    def test_availabilityrooms_url(self):
        url = reverse('availability-rooms')
        self.assertEquals(
            resolve(url).func.view_class, views.RoomAvailabilityView
        )

    def test_cancelbook_url(self):
        url = reverse('cancel-book', args=[1])
        self.assertEquals(
            resolve(url).func.view_class, views.CancelBookingView
        )
