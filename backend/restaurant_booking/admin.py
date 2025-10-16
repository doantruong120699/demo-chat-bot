from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Table, Booking


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'table_type', 'capacity', 'floor', 
        'status', 'is_available_for_booking', 'created_at', 'updated_at'
    ]
    list_filter = [
        'table_type', 'status', 'floor', 
    ]
    search_fields = ['notes']
    list_editable = ['status']
    ordering = ['floor', 'id']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('table_type', 'capacity', 'floor', )
        }),
        ('Status & Availability', {
            'fields': ('status',)
        }),
        ('Dimensions (Optional)', {
            'fields': ('width', 'length'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def is_available_for_booking(self, obj):
        if obj.status == Table.TableStatus.AVAILABLE:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Available</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Not Available</span>'
            )
    is_available_for_booking.short_description = 'Available for Booking'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'guest_name', 'table_display', 'booking_date',
        'booking_time', 'party_size', 'status', 'source', 'created_at', 'updated_at'
    ]
    list_filter = [
        'status', 'source', 'booking_date', 'table__table_type', 'table__floor'
    ]
    search_fields = [
        'guest_name', 'guest_email', 'guest_phone'
    ]
    list_editable = ['status']
    ordering = ['-created_at']

    fieldsets = (
        ('Booking Information', {
            'fields': (
                'table', 'booking_date', 'booking_time', 'duration_hours',
                'party_size', 'status', 'source'
            )
        }),
        ('Guest Information', {
            'fields': (
                'guest_name', 'guest_email', 'guest_phone'
            )
        }),
        ('Internal Notes', {
            'fields': (
                'notes', 
            ),
            'classes': ('collapse',)
        }),
        ('Status & Confirmation', {
            'fields': (
                'cancellation_reason',
            ),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = [
        'created_at', 'updated_at',
    ]

    def table_display(self, obj):
        return f"Table {obj.table.id} ({obj.table.get_table_type_display()})"
    table_display.short_description = 'Table'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('table')

    actions = ['mark_confirmed', 'mark_cancelled', 'mark_completed', 'mark_no_show']

    def mark_confirmed(self, request, queryset):
        updated = queryset.filter(status=Booking.BookingStatus.PENDING).update(
            status=Booking.BookingStatus.CONFIRMED
        )
        self.message_user(request, f'{updated} bookings marked as confirmed.')
    mark_confirmed.short_description = 'Mark selected bookings as confirmed'

    def mark_cancelled(self, request, queryset):
        updated = queryset.exclude(status=Booking.BookingStatus.CANCELLED).update(
            status=Booking.BookingStatus.CANCELLED
        )
        self.message_user(request, f'{updated} bookings marked as cancelled.')
    mark_cancelled.short_description = 'Mark selected bookings as cancelled'

    def mark_completed(self, request, queryset):
        updated = queryset.filter(status=Booking.BookingStatus.CONFIRMED).update(
            status=Booking.BookingStatus.COMPLETED
        )
        self.message_user(request, f'{updated} bookings marked as completed.')
    mark_completed.short_description = 'Mark selected bookings as completed'

    def mark_no_show(self, request, queryset):
        updated = queryset.filter(status=Booking.BookingStatus.CONFIRMED).update(
            status=Booking.BookingStatus.NO_SHOW
        )
        self.message_user(request, f'{updated} bookings marked as no show.')
    mark_no_show.short_description = 'Mark selected bookings as no show'


# Customize admin site
admin.site.site_header = "Restaurant Booking System"
admin.site.site_title = "Restaurant Admin"
admin.site.index_title = "Restaurant Management"

