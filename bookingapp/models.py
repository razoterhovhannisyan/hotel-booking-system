from django.db import models
from authapp.models import User


class Room(models.Model):
    number = models.IntegerField(unique=True)
    cost_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"Room number: {self.number} id - {self.id}"


class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.room} - "
            f"{self.user.first_name} {self.user.last_name} id - {self.id}"
        )
