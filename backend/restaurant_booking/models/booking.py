from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from common.models.base import DateTimeModel, SoftDeleteModel
import random
import string


class Booking(DateTimeModel, SoftDeleteModel):
    """
    Booking model to store restaurant booking information
    """

    class BookingStatus(models.TextChoices):
        PENDING = "PENDING", "Chờ xác nhận"
        CONFIRMED = "CONFIRMED", "Đã xác nhận"
        CANCELLED = "CANCELLED", "Đã hủy"
        COMPLETED = "COMPLETED", "Hoàn thành"
        NO_SHOW = "NO_SHOW", "Không đến"

    class BookingSource(models.TextChoices):
        WEBSITE = "WEBSITE", "Website"
        PHONE = "PHONE", "Điện thoại"
        WALK_IN = "WALK_IN", "Đến trực tiếp"
        MOBILE_APP = "MOBILE_APP", "Ứng dụng di động"
        THIRD_PARTY = "THIRD_PARTY", "Bên thứ ba"

    # Basic booking information
    table = models.ForeignKey(
        'restaurant_booking.Table',
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Bàn"
    )

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã đặt bàn",
        editable=False,
        default=''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    )

    # Guest information (for non-registered users)
    guest_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Tên khách"
    )
    guest_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email khách"
    )
    guest_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Số điện thoại khách"
    )

    # Booking details
    booking_date = models.DateField(verbose_name="Ngày đặt bàn")
    booking_time = models.TimeField(verbose_name="Giờ đặt bàn")
    duration_hours = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=2.0,
        validators=[MinValueValidator(0.5), MaxValueValidator(8.0)],
        verbose_name="Thời gian (giờ)"
    )

    # Party information
    party_size = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        verbose_name="Số người"
    )

    # Booking status and source
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
        verbose_name="Trạng thái"
    )
    source = models.CharField(
        max_length=20,
        choices=BookingSource.choices,
        default=BookingSource.WEBSITE,
        verbose_name="Nguồn đặt bàn"
    )

    # Confirmation and notes
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Ghi chú nội bộ"
    )
    
    # Cancellation information
    cancellation_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name="Lý do hủy"
    )

    class Meta:
        db_table = 'restaurant_bookings'
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ['-created_at']

    def __str__(self):
        guest_name = self.guest_name or "Guest"
        return f"Table {self.table.id} - {guest_name} - {self.booking_date} {self.booking_time}"

    def save(self, *args, **kwargs):
        # Generate unique booking code if not exists
        if not self.code:
            self.code = self._generate_unique_code('code')
        super().save(*args, **kwargs)

    def _generate_unique_code(self, field, length=8):
        """
        Generate a unique code for the specified field.
        """
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            if not Booking.objects.filter(**{field: code}).exists():
                return code

    @property
    def customer_name(self):
        """Get customer name (guest only)"""
        return self.guest_name or "Guest"

    @property
    def customer_email(self):
        """Get customer email (guest only)"""
        return self.guest_email

    @property
    def customer_phone(self):
        """Get customer phone (guest only)"""
        return self.guest_phone

    @property
    def is_upcoming(self):
        """Check if booking is in the future"""
        from datetime import datetime
        booking_datetime = datetime.combine(self.booking_date, self.booking_time)
        return booking_datetime > timezone.now()

    @property
    def is_past(self):
        """Check if booking is in the past"""
        from datetime import datetime, timedelta
        booking_datetime = datetime.combine(self.booking_date, self.booking_time)
        end_datetime = booking_datetime + timedelta(hours=float(self.duration_hours))
        return end_datetime < timezone.now()

    @property
    def can_be_cancelled(self):
        """Check if booking can be cancelled"""
        if self.status in [self.BookingStatus.CANCELLED, self.BookingStatus.COMPLETED]:
            return False

        # Check if booking is within cancellation window
        from datetime import datetime, timedelta
        booking_datetime = datetime.combine(self.booking_date, self.booking_time)
        cancellation_deadline = booking_datetime - timedelta(hours=2)  # 2 hours before
        return timezone.now() < cancellation_deadline

    @property
    def booking_datetime(self):
        """Get booking datetime"""
        from datetime import datetime
        return datetime.combine(self.booking_date, self.booking_time)

    @property
    def end_datetime(self):
        """Get booking end datetime"""
        from datetime import timedelta
        return self.booking_datetime + timedelta(hours=float(self.duration_hours))

    def cancel(self, reason=None, cancelled_by=None):
        """Cancel the booking"""
        if self.can_be_cancelled:
            self.status = self.BookingStatus.CANCELLED
            self.cancellation_reason = reason
            self.cancelled_by = cancelled_by or ""
            self.cancelled_at = timezone.now()
            self.save()
            return True
        return False
