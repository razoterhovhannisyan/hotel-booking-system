from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from bookingapp import models as booking_models
from authapp import models as auth_models
from bookingapp import serializers
from datetime import datetime
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


class RoomListViewTest(APITestCase):
    def setUp(self):
        self.user_1 = auth_models.User.objects.create(
            email='artur@mail.ru',
            password='artoarto',
            first_name='Artur',
            last_name='Arturyan',
            is_staff=False,
            is_active=True
        )
        self.refresh = RefreshToken.for_user(self.user_1)
        self.access_token = str(self.refresh.access_token)
        self.room_1 = booking_models.Room.objects.create(
            number=15,
            cost_per_day=100,
            capacity=3
        )
        self.room_2 = booking_models.Room.objects.create(
            number=16,
            cost_per_day=120,
            capacity=4
        )

    def test_roomlisview_get(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        response = self.client.get(reverse('all-rooms'))
        response_data = response.data
        serializer_data = serializers.RoomListSerializer(
            [self.room_1, self.room_2], many=True
        ).data
        self.assertEqual(serializer_data, response_data)


class RoomDetailViewTest(APITestCase):
    def setUp(self):
        self.user_1 = auth_models.User.objects.create(
            email='artur@mail.ru',
            password='artoarto',
            first_name='Artur',
            last_name='Arturyan',
            is_staff=False,
            is_active=True
        )
        self.refresh = RefreshToken.for_user(self.user_1)
        self.access_token = str(self.refresh.access_token)
        self.room_1 = booking_models.Room.objects.create(
            number=15,
            cost_per_day=100,
            capacity=3
        )
        self.room_2 = booking_models.Room.objects.create(
            number=16,
            cost_per_day=120,
            capacity=4
        )

    def test_roomdetailview_get(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        response = self.client.get(
            reverse('room-details', args=[self.room_1.id])
        )
        response_data = response.data
        serializer_data = serializers.RoomListSerializer(self.room_1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response_data)

    def test_roomdetailview_get_non_existing_room(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        response = self.client.get(reverse('room-details', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data,
            {'detail': 'No Room matches the given query.'}
        )


class GetBookingView(APITestCase):
    def setUp(self):
        self.user_1 = auth_models.User.objects.create_user(
            email='artur@mail.ru',
            password='artoarto',
            first_name='Artur',
            last_name='Arturyan',
            is_staff=False,
            is_active=True
        )

        self.refresh = RefreshToken.for_user(self.user_1)
        self.access_token = str(self.refresh.access_token)
        self.room_1 = booking_models.Room.objects.create(
            number=101,
            cost_per_day=150.00,
            capacity=2
        )
        self.booking_1 = booking_models.Booking.objects.create(
            user=self.user_1,
            room=self.room_1,
            start_date=timezone.make_aware(datetime(2024, 7, 20)),
            end_date=timezone.make_aware(datetime(2024, 7, 27)),
            is_cancelled=False
        )

    def test_get_bookings_auth(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        response = self.client.get(reverse('my-bookings'))
        response_data = response.data
        serializer_data = serializers.BookingSerializer(
            [self.booking_1], many=True
        ).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, serializer_data)

    def test_get_bookings_noauth(self):
        response = self.client.get(reverse('my-bookings'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RoomFilterSortTest(APITestCase):
    def setUp(self):
        self.user_1 = auth_models.User.objects.create_user(
            email='artur@mail.ru',
            password='artoarto',
            first_name='Artur',
            last_name='Arturyan',
            is_staff=False,
            is_active=True
        )

        self.refresh = RefreshToken.for_user(self.user_1)
        self.access_token = str(self.refresh.access_token)
        self.room_1 = booking_models.Room.objects.create(
            number=101,
            cost_per_day=150.00,
            capacity=2
        )
        self.room_2 = booking_models.Room.objects.create(
            number=102,
            cost_per_day=150.00,
            capacity=4
        )
        self.room_3 = booking_models.Room.objects.create(
            number=103,
            cost_per_day=200.00,
            capacity=3
        )

    def test_filter_min_price(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        response = self.client.get(reverse('room-filter'), {'min_price': 150})
        filtered_rooms = booking_models.Room.objects.filter(
            cost_per_day__gte=150
        )
        expected_data = serializers.RoomListSerializer(
            filtered_rooms, many=True
        ).data
        response_data_sorted = sorted(response.data, key=lambda x: x['number'])
        expected_data_sorted = sorted(expected_data, key=lambda x: x['number'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data_sorted, expected_data_sorted)

    def test_filter_max_price(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        response = self.client.get(reverse('room-filter'), {'max_price': 150})
        expected_rooms = [self.room_1, self.room_2]
        expected_data = serializers.RoomListSerializer(
            expected_rooms, many=True
        ).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_filter_capacity(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        response = self.client.get(reverse('room-filter'), {'capacity': 3})
        expected_rooms = [self.room_3]
        expected_data = serializers.RoomListSerializer(
            expected_rooms, many=True
        ).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_sort_price(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        response = self.client.get(
            reverse('room-filter'), {'sort_by': 'price'}
        )
        expected_rooms = [self.room_1, self.room_2, self.room_3]
        expected_data = serializers.RoomListSerializer(
            expected_rooms, many=True
        ).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_sort_capacity(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        response = self.client.get(
            reverse('room-filter'), {'ordering': 'capacity'}
        )
        expected_rooms = [self.room_1, self.room_3, self.room_2]
        expected_data = serializers.RoomListSerializer(
            expected_rooms, many=True
        ).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_no_authentication(self):
        response = self.client.get(reverse('room-filter'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RoomAvailabilityTest(APITestCase):
    def setUp(self):
        self.user_1 = auth_models.User.objects.create_user(
            email='artur@mail.ru',
            password='artoarto',
            first_name='Artur',
            last_name='Arturyan',
            is_staff=False,
            is_active=True
        )

        self.user_2 = auth_models.User.objects.create_user(
            email='vazgen@mail.ru',
            password='vazgvazg',
            first_name='Vazgen',
            last_name='Vazgenyan'
        )
        self.refresh = RefreshToken.for_user(self.user_1)
        self.access_token = str(self.refresh.access_token)

        self.refresh_user_2 = RefreshToken.for_user(self.user_2)
        self.access_token_user_2 = str(self.refresh_user_2.access_token)

        self.room_1 = booking_models.Room.objects.create(
            number=101,
            cost_per_day=100,
            capacity=2
        )
        self.room_2 = booking_models.Room.objects.create(
            number=102,
            cost_per_day=150,
            capacity=4
        )

        self.booking_1 = booking_models.Booking.objects.create(
            room=self.room_2,
            user=self.user_1,
            start_date=timezone.make_aware(datetime(2024, 7, 29, 12, 0, 0)),
            end_date=timezone.make_aware(datetime(2024, 7, 30, 12, 0, 0)),
            is_cancelled=False
        )
        self.booking_2 = booking_models.Booking.objects.create(
            room=self.room_1,
            user=self.user_2,
            start_date=timezone.make_aware(datetime(2024, 7, 22, 12, 0, 0)),
            end_date=timezone.make_aware(datetime(2024, 7, 25, 12, 0, 0)),
            is_cancelled=False
        )

    def test_room_availability(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        start_date = timezone.make_aware(
            datetime(2024, 7, 28, 12, 0, 0)
        ).isoformat()
        end_date = timezone.make_aware(
            datetime(2024, 7, 30, 12, 0, 0)
        ).isoformat()
        response = self.client.get(
            reverse('availabilityrooms-list'),
            {'start_date': start_date, 'end_date': end_date}
        )
        expected_data = [{'number': self.room_1.number}]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_room_availability_no_rooms(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        start_date = timezone.make_aware(
            datetime(2024, 7, 20, 12, 0, 0)
        ).isoformat()
        end_date = timezone.make_aware(
            datetime(2024, 7, 30, 12, 0, 0)
        ).isoformat()
        response = self.client.get(
            reverse('availabilityrooms-list'),
            {'start_date': start_date, 'end_date': end_date}
        )
        expected_data = []
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_invalid_dates(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        response = self.client.get(
            reverse('availabilityrooms-list'),
            {'start_date': 'invalid-date', 'end_date': 'invalid-date'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('start_date', response.data)
        self.assertIn('end_date', response.data)
