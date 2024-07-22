from django.db.models import Q
from rest_framework.views import APIView
from . import models
from . import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
# Create your views here.


class RoomListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        rooms = models.Room.objects.all()
        serializer = serializers.RoomListSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        try:
            room = models.Room.objects.get(id=pk)
            serializer = serializers.RoomListSerializer(room)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Room.DoesNotExist:
            return Response({'error':'Room not found'}, status=status.HTTP_404_NOT_FOUND)



class RoomBookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        data=request.data.copy()
        data['user'] = user.id

        serializer = serializers.BookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GetBookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        bookings = models.Booking.objects.filter(user=user)
        serializer = serializers.BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class RoomFilterSortView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        rooms = models.Room.objects.all()

        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        if min_price is not None:
            rooms = rooms.filter(cost_per_day__gte=min_price)
        if max_price is not None:
            rooms = rooms.filter(cost_per_day__lte=max_price)

        capacity = request.query_params.get('capacity')
        if capacity is not None:
            rooms = rooms.filter(capacity=capacity)

        sort_by = request.query_params.get('sort_by')
        if sort_by == 'price':
            rooms = rooms.order_by('cost_per_day')
        elif sort_by == 'capacity':
            rooms = rooms.order_by('capacity')

        serializer = serializers.RoomListSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class RoomAvailabilityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = serializers.RoomAvailabilitySerializer(data=request.query_params)
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']

            if end_date <= start_date:
                return Response({'error':'end_date must be after start_date'}, status=status.HTTP_400_BAD_REQUEST)

            booked_rooms = models.Booking.objects.filter(
                start_date__lt=end_date,
                end_date__gt=start_date,
                is_cancelled=False
            ).values_list('room_id', flat=True)

            available_rooms = models.Room.objects.exclude(id__in=booked_rooms)

            available_rooms_data = [
                {
                    'number': room.number,
                }
                for room in available_rooms
            ]

            return Response(available_rooms_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CancelBookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            booking = models.Booking.objects.get(id=pk)
        except models.Booking.DoesNotExist:
            return Response({'detail':'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user != booking.user:
            return Response({'detail':'You dont have permission to cancel this book'}, status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.CancelBookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            is_cancelled = serializer.validated_data.get('is_cancelled')
            if is_cancelled:
                booking.delete()
                return Response({'detail': 'Booking cancelled successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail':'Booking not cancelled'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
