from rest_framework import serializers
from . import models
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['number', 'cost_per_day', 'capacity']



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        fields = ['room', 'start_date', 'end_date', 'is_cancelled']


    def validate(self, data):
        room = data.get('room')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date >= end_date:
            raise serializers.ValidationError('End date must be after start date.')


        if models.Booking.objects.filter(
            room=room,
            start_date__lt=end_date,
            end_date__gt=start_date,
            is_cancelled=False).exists():
            raise serializers.ValidationError('The room is not available for the selected dates.')

        return data


class CancelBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        fields = ['is_cancelled']



class RoomAvailabilitySerializer(serializers.Serializer):
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
