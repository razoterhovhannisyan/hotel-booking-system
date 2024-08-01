from django.test import TestCase
from bookingapp import models as booking_models
from authapp import models as auth_models
from datetime import date
from datetime import datetime
from django.utils import timezone


class RoomModelTest(TestCase):
    def setUp(self):
        self.room = booking_models.Room.objects.create(
            number=101,
            cost_per_day=150.00,
            capacity=2
        )

    def test_room_str(self):
        self.assertTrue(str(self.room).startswith("Room number: 101 id -"))

    def test_room_fields(self):
        self.assertEqual(self.room.number, 101)
        self.assertEqual(self.room.cost_per_day, 150.00)
        self.assertEqual(self.room.capacity, 2)


class BookingModelTest(TestCase):

    def setUp(self):
        self.user = auth_models.User.objects.create(
            email="peto@mail.ru",
            first_name="Petros",
            last_name="Petrosyan",
            is_staff=False,
            is_active=True
        )
        self.room = booking_models.Room.objects.create(
            number=102,
            cost_per_day=200.00,
            capacity=3
        )
        self.booking = booking_models.Booking.objects.create(
            user=self.user,
            room=self.room,
            start_date=timezone.make_aware(datetime(2024, 7, 20, 12, 0, 0)),
            end_date=timezone.make_aware(datetime(2024, 7, 27, 12, 0, 0)),
            is_cancelled=False
        )

    def test_booking_str(self):
        self.assertTrue(str(self.booking).startswith("Room number: 102 id -"))

    def test_booking_fields(self):
        self.assertEqual(self.booking.user, self.user)
        self.assertEqual(self.booking.room, self.room)
        self.assertEqual(
            self.booking.start_date,
            timezone.make_aware(datetime(2024, 7, 20, 12, 0, 0))
        )
        self.assertEqual(
            self.booking.end_date,
            timezone.make_aware(datetime(2024, 7, 27, 12, 0, 0))
        )
        self.assertFalse(self.booking.is_cancelled)
