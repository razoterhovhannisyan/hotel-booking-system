import django_filters
from . import models


class RoomFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name='cost_per_day',
        lookup_expr='gte'
    )
    max_price = django_filters.NumberFilter(
        field_name='cost_per_day',
        lookup_expr='lte'
    )
    capacity = django_filters.NumberFilter(field_name='capacity')
    ordering = django_filters.OrderingFilter(
        fields=(
            ('cost_per_day', 'price'),
            ('capacity', 'capacity'),
        )
    )

    class Meta:
        model = models.Room
        fields = ['min_price', 'max_price', 'capacity']


class BookingFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(
        field_name='start_date',
        lookup_expr='gte'
    )
    end_date = django_filters.DateTimeFilter(
        field_name='end_date',
        lookup_expr='lte'
    )

    class Meta:
        model = models.Booking
        fields = ['start_date', 'end_date']
