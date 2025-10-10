from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from common.models.base import DateTimeModel, SoftDeleteModel


class Table(DateTimeModel, SoftDeleteModel):
    """
    Table model to store restaurant table information
    """

    class TableType(models.TextChoices):
        INDOOR = "INDOOR", "Trong nhà"
        OUTDOOR = "OUTDOOR", "Ngoài trời"
        PRIVATE = "PRIVATE", "Phòng riêng"
        BAR = "BAR", "Quầy bar"
        BOOTH = "BOOTH", "Ghế ngồi"
        WINDOW = "WINDOW", "Cửa sổ"

    class TableStatus(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Có sẵn"
        OCCUPIED = "OCCUPIED", "Đang sử dụng"
        RESERVED = "RESERVED", "Đã đặt"
        MAINTENANCE = "MAINTENANCE", "Bảo trì"

    # Table specifications
    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        verbose_name="Sức chứa",
    )
    table_type = models.CharField(
        max_length=20,
        choices=TableType.choices,
        default=TableType.INDOOR,
        verbose_name="Loại bàn",
    )

    # Location within restaurant
    floor = models.PositiveIntegerField(default=1, verbose_name="Tầng")

    # Table status
    status = models.CharField(
        max_length=20,
        choices=TableStatus.choices,
        default=TableStatus.AVAILABLE,
        verbose_name="Trạng thái",
    )

    # Table dimensions (optional)
    width = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Chiều rộng (mét)",
    )
    length = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Chiều dài (mét)",
    )

    # Additional notes
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")

    class Meta:
        db_table = "restaurant_tables"
        verbose_name = "Table"
        verbose_name_plural = "Tables"
        ordering = ["floor", "id"]

    def __str__(self):
        return f"Table {self.id}"

    @property
    def is_available_for_booking(self):
        """Check if table is available for booking"""
        return self.status == self.TableStatus.AVAILABLE

    def get_available_slots(self, date, duration_hours=2):
        """Get available time slots for a specific date"""
        from django.utils import timezone
        from datetime import datetime, timedelta
        from .booking import Booking

        # Restaurant operating hours (assuming standard hours)
        from datetime import time

        opening_time = time(9, 0)  # 9:00 AM
        closing_time = time(22, 0)  # 10:00 PM

        # Convert to datetime for the specific date
        start_datetime = datetime.combine(date, opening_time)
        end_datetime = datetime.combine(date, closing_time)

        # Get existing bookings for this table on this date
        existing_bookings = Booking.objects.filter(
            table=self,
            booking_date=date,
            status__in=[Booking.BookingStatus.CONFIRMED, Booking.BookingStatus.PENDING],
        ).order_by("booking_time")

        available_slots = []
        current_time = start_datetime

        for booking in existing_bookings:
            booking_start = datetime.combine(date, booking.booking_time)
            booking_end = booking_start + timedelta(hours=booking.duration_hours)

            # Add slot if there's time before this booking
            if current_time + timedelta(hours=duration_hours) <= booking_start:
                available_slots.append(current_time.time())

            # Move current time to after this booking
            current_time = booking_end

        # Add remaining time slots
        while current_time + timedelta(hours=duration_hours) <= end_datetime:
            available_slots.append(current_time.time())
            current_time += timedelta(hours=1)  # Check every hour

        return available_slots
