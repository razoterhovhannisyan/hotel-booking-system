from . import models, serializers, filters
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action


class RoomListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.RoomFilter


class RoomDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomListSerializer


class RoomBookingView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        user = request.user
        data = request.data.copy()
        data['user'] = user.id

        serializer = serializers.BookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class GetBookingView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.BookingSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.BookingFilter

    def get_queryset(self):
        user = self.request.user
        return models.Booking.objects.filter(user=user)


class RoomFilterSortView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.RoomListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.RoomFilter

    def get_queryset(self):
        return models.Room.objects.all()


class RoomAvailabilityView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        serializer = serializers.RoomAvailabilitySerializer(
            data=request.query_params
        )
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']

            booked_rooms = models.Booking.objects.filter(
                start_date__lt=end_date,
                end_date__gt=start_date,
                is_cancelled=False
            ).values_list('room_id', flat=True)

            available_rooms = models.Room.objects.exclude(id__in=booked_rooms)
            available_rooms_data = [
                {'number': room.number}
                for room in available_rooms
            ]
            return Response(available_rooms_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelBookingView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk):
        try:
            booking = models.Booking.objects.get(id=pk)
        except models.Booking.DoesNotExist:
            return Response(
                {'detail': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user != booking.user:
            return Response(
                {'detail': 'You dont have permission to cancel this book'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = serializers.CancelBookingSerializer(
            booking,
            data=request.data
        )
        if serializer.is_valid():
            is_cancelled = serializer.validated_data.get('is_cancelled')
            if is_cancelled:
                booking.delete()
                return Response(
                    {'detail': 'Booking cancelled successfully'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'detail': 'Booking not cancelled'},
                    status=status.HTTP_200_OK
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
