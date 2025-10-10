from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Table, Booking
from accounts.models.user import User
from restaurant_booking.services.chat import RestaurantBookingChatService
from restaurant_booking.serializers import RestaurantBookingChatRequestSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def restaurant_chat_stream(request):
    serializer = RestaurantBookingChatRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    chat_service = RestaurantBookingChatService()

    response = StreamingHttpResponse(
        chat_service.chat(request, serializer.validated_data),
        content_type="text/event-stream",
    )
    response["Cache-Control"] = "no-cache"
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Headers"] = "Cache-Control"

    return response

@api_view(['GET'])
@permission_classes([AllowAny])
def table_list(request):
    """
    Get list of all tables, grouped by floor, with optional filters and status for a specific date.
    No pagination. If 'date' is provided, status will reflect booking status for that date.
    """
    try:
        tables = Table.objects.filter(is_deleted=False).order_by('floor', 'id')
        date_str = request.GET.get('date')  # Expecting YYYY-MM-DD

        # Prepare date filter for booking status
        booking_date = None
        if date_str:
            try:
                booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except Exception:
                return Response({
                    'error': 'Invalid date format. Use YYYY-MM-DD.'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Group tables by floor
        floors = {}
        for table in tables:
            # Default status
            table_status = table.get_status_display()
            is_available_for_booking = table.is_available_for_booking

            # If date is provided, check if table is booked on that date
            if booking_date:
                has_booking = Booking.objects.filter(
                    table=table,
                    booking_date=booking_date,
                    status__in=[Booking.BookingStatus.CONFIRMED, Booking.BookingStatus.PENDING]
                ).exists()
                if has_booking:
                    table_status = "Booked"
                    is_available_for_booking = False
                else:
                    table_status = "Available"
                    is_available_for_booking = True

            table_data = {
                'id': table.id,
                'table_type': table.get_table_type_display(),
                'capacity': table.capacity,
                'floor': table.floor,
                'status': table_status,
                'is_available_for_booking': is_available_for_booking,
                'created_at': table.created_at.isoformat(),
                'notes': table.notes
            }

            floor_key = f"Floor {table.floor}"
            if floor_key not in floors:
                floors[floor_key] = []
            floors[floor_key].append(table_data)

        # Convert to list of dicts as in the example
        floors_list = []
        for floor_name, tables_list in floors.items():
            floors_list.append({
                "name": floor_name,
                "tables": tables_list
            })

        return Response(floors_list)

    except Exception as e:
        return Response({
            'error': f'Failed to fetch tables: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def table_search(request):
    """Search for available tables"""
    try:
        data = request.data
        
        party_size = data.get('party_size')
        booking_date = data.get('booking_date')
        booking_time = data.get('booking_time')
        table_type = data.get('table_type')
        floor = data.get('floor')
        wheelchair_accessible = data.get('wheelchair_accessible')
        
        if not party_size or not booking_date:
            return Response({
                'error': 'party_size and booking_date are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse date
        booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
        
        # Build query
        query = Q(status=Table.TableStatus.AVAILABLE, is_deleted=False)
        query &= Q(capacity__gte=party_size)
        
        if table_type:
            query &= Q(table_type=table_type)
        if floor:
            query &= Q(floor=floor)
        if wheelchair_accessible is not None:
            query &= Q(is_wheelchair_accessible=wheelchair_accessible)
        
        available_tables = Table.objects.filter(query).order_by('capacity', 'floor')
        
        # Check for time conflicts if time is provided
        if booking_time:
            booking_time_obj = datetime.strptime(booking_time, "%H:%M").time()
            conflicting_bookings = Booking.objects.filter(
                booking_date=booking_date_obj,
                status__in=[Booking.BookingStatus.CONFIRMED, Booking.BookingStatus.PENDING]
            )
            
            final_tables = []
            for table in available_tables:
                has_conflict = False
                for booking in conflicting_bookings.filter(table=table):
                    booking_start = datetime.combine(booking_date_obj, booking.booking_time)
                    booking_end = booking_start + timezone.timedelta(hours=float(booking.duration_hours))
                    requested_start = datetime.combine(booking_date_obj, booking_time_obj)
                    requested_end = requested_start + timezone.timedelta(hours=2)
                    
                    if (requested_start < booking_end and requested_end > booking_start):
                        has_conflict = True
                        break
                
                if not has_conflict:
                    final_tables.append(table)
            
            available_tables = final_tables
        
        tables_data = []
        for table in available_tables:
            table_data = {
                'id': table.id,
                'table_type': table.get_table_type_display(),
                'capacity': table.capacity,
                'floor': table.floor,
                'status': table.get_status_display(),
                'is_available_for_booking': table.is_available_for_booking,
                'notes': table.notes
            }
            tables_data.append(table_data)
        
        return Response({
            'available_tables': tables_data,
            'search_criteria': {
                'party_size': party_size,
                'booking_date': booking_date,
                'booking_time': booking_time,
                'table_type': table_type,
                'floor': floor,
                'wheelchair_accessible': wheelchair_accessible
            }
        })
        
    except Exception as e:
        return Response({
            'error': f'Table search failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def table_detail(request, table_id):
    """Get table details"""
    try:
        table = get_object_or_404(Table, id=table_id, is_deleted=False)
        
        table_data = {
            'id': table.id,
            'table_type': table.get_table_type_display(),
            'capacity': table.capacity,
            'floor': table.floor,
            'status': table.get_status_display(),
            'is_available_for_booking': table.is_available_for_booking,
            'width': float(table.width) if table.width else None,
            'length': float(table.length) if table.length else None,
            'notes': table.notes,
            'created_at': table.created_at.isoformat(),
            'updated_at': table.updated_at.isoformat()
        }
        
        return Response(table_data)
        
    except Exception as e:
        return Response({
            'error': f'Failed to fetch table details: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def booking_list(request):
    """Get list of bookings"""
    try:
        bookings = Booking.objects.filter(is_deleted=False).order_by('-created_at')
        
        # Apply filters
        customer_id = request.GET.get('customer_id')
        booking_date = request.GET.get('booking_date')
        status_filter = request.GET.get('status')
        code = request.GET.get('code')
        
        if customer_id:
            bookings = bookings.filter(customer_id=customer_id)
        if booking_date:
            booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
            bookings = bookings.filter(booking_date=booking_date_obj)
        if status_filter:
            bookings = bookings.filter(status=status_filter)
        if code:
            bookings = bookings.filter(code=code)
        
        # Pagination
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 20)
        paginator = Paginator(bookings, page_size)
        page_obj = paginator.get_page(page)
        
        bookings_data = []
        for booking in page_obj:
            booking_data = {
                'id': booking.id,
                'code': booking.code,
                'customer_name': booking.customer_name,
                'table_id': booking.table.id,
                'table_type': booking.table.get_table_type_display(),
                'booking_date': booking.booking_date.strftime("%Y-%m-%d"),
                'booking_time': booking.booking_time.strftime("%H:%M"),
                'party_size': booking.party_size,
                'duration_hours': float(booking.duration_hours),
                'status': booking.get_status_display(),
                'source': booking.get_source_display(),
                'created_at': booking.created_at.isoformat()
            }
            bookings_data.append(booking_data)
        
        return Response({
            'bookings': bookings_data,
            'pagination': {
                'page': page_obj.number,
                'pages': paginator.num_pages,
                'total': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous()
            }
        })
        
    except Exception as e:
        return Response({
            'error': f'Failed to fetch bookings: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def booking_create(request):
    """Create a new booking"""
    try:
        data = request.data
        
        # Required fields
        table_id = data.get('table_id')
        booking_date = data.get('booking_date')
        booking_time = data.get('booking_time')
        party_size = data.get('party_size')
        
        if not all([table_id, booking_date, booking_time, party_size]):
            return Response({
                'error': 'table_id, booking_date, booking_time, and party_size are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse date and time
        booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
        booking_time_obj = datetime.strptime(booking_time, "%H:%M").time()
        
        # Get table
        table = get_object_or_404(Table, id=table_id, is_deleted=False)
        
        # Check if table is available
        if table.status != Table.TableStatus.AVAILABLE:
            return Response({
                'error': f'Table {table_id} is not available (status: {table.get_status_display()})'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check for time conflicts
        conflicting_bookings = Booking.objects.filter(
            table=table,
            booking_date=booking_date_obj,
            status__in=[Booking.BookingStatus.CONFIRMED, Booking.BookingStatus.PENDING]
        )
        
        duration_hours = float(data.get('duration_hours', 2.0))
        for booking in conflicting_bookings:
            booking_start = datetime.combine(booking_date_obj, booking.booking_time)
            booking_end = booking_start + timezone.timedelta(hours=float(booking.duration_hours))
            requested_start = datetime.combine(booking_date_obj, booking_time_obj)
            requested_end = requested_start + timezone.timedelta(hours=duration_hours)
            
            if (requested_start < booking_end and requested_end > booking_start):
                return Response({
                    'error': f'Table {table_id} is already booked during this time'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get customer if provided
        customer = None
        customer_id = data.get('customer_id')
        if customer_id:
            customer = get_object_or_404(User, id=customer_id)
        
        # Create booking
        booking = Booking.objects.create(
            table=table,
            customer=customer,
            guest_name=data.get('guest_name'),
            guest_email=data.get('guest_email'),
            guest_phone=data.get('guest_phone'),
            booking_date=booking_date_obj,
            booking_time=booking_time_obj,
            party_size=party_size,
            duration_hours=duration_hours,
            contact_phone=data.get('guest_phone') or (customer.phone if customer and hasattr(customer, 'phone') else ''),
            contact_email=data.get('guest_email') or (customer.email if customer else ''),
            status=Booking.BookingStatus.PENDING
        )
        
        booking_data = {
            'id': booking.id,
            'code': booking.code,
            'customer_name': booking.customer_name,
            'table_id': booking.table.id,
            'table_type': booking.table.get_table_type_display(),
            'booking_date': booking.booking_date.strftime("%Y-%m-%d"),
            'booking_time': booking.booking_time.strftime("%H:%M"),
            'party_size': booking.party_size,
            'duration_hours': float(booking.duration_hours),
            'status': booking.get_status_display(),
            'created_at': booking.created_at.isoformat()
        }
        
        return Response(booking_data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Failed to create booking: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def booking_detail(request, booking_id):
    """Get booking details"""
    try:
        booking = get_object_or_404(Booking, id=booking_id, is_deleted=False)
        
        booking_data = {
            'id': booking.id,
            'code': booking.code,
            'customer_name': booking.customer_name,
            'customer_email': booking.customer_email,
            'customer_phone': booking.customer_phone,
            'table_id': booking.table.id,
            'table_type': booking.table.get_table_type_display(),
            'table_floor': booking.table.floor,
            'booking_date': booking.booking_date.strftime("%Y-%m-%d"),
            'booking_time': booking.booking_time.strftime("%H:%M"),
            'party_size': booking.party_size,
            'duration_hours': float(booking.duration_hours),
            'status': booking.get_status_display(),
            'source': booking.get_source_display(),
            'dietary_restrictions': booking.dietary_restrictions,
            'contact_phone': booking.contact_phone,
            'contact_email': booking.contact_email,
            'notes': booking.notes,
            'cancellation_reason': booking.cancellation_reason,
            'created_at': booking.created_at.isoformat(),
            'updated_at': booking.updated_at.isoformat()
        }
        
        return Response(booking_data)
        
    except Exception as e:
        return Response({
            'error': f'Failed to fetch booking details: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def booking_cancel(request, booking_id):
    """Cancel a booking"""
    try:
        booking = get_object_or_404(Booking, id=booking_id, is_deleted=False)
        
        if booking.status in [Booking.BookingStatus.CANCELLED, Booking.BookingStatus.COMPLETED]:
            return Response({
                'error': f'Booking {booking_id} cannot be cancelled (status: {booking.get_status_display()})'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        cancellation_reason = request.data.get('cancellation_reason', '')
        cancelled_by_id = request.data.get('cancelled_by_id')
        
        cancelled_by = None
        if cancelled_by_id:
            cancelled_by = get_object_or_404(User, id=cancelled_by_id)
        
        success = booking.cancel(cancellation_reason, cancelled_by)
        
        if success:
            return Response({
                'message': f'Booking {booking_id} has been cancelled successfully',
                'booking_id': booking.id,
                'status': booking.get_status_display(),
                'cancelled_at': booking.cancelled_at.isoformat() if booking.cancelled_at else None
            })
        else:
            return Response({
                'error': f'Booking {booking_id} cannot be cancelled at this time'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'error': f'Failed to cancel booking: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def booking_confirm(request, booking_id):
    """Confirm a booking"""
    try:
        booking = get_object_or_404(Booking, id=booking_id, is_deleted=False)
        
        if booking.status != Booking.BookingStatus.PENDING:
            return Response({
                'error': f'Booking {booking_id} cannot be confirmed (status: {booking.get_status_display()})'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        success = booking.confirm()
        
        if success:
            return Response({
                'message': f'Booking {booking_id} has been confirmed successfully',
                'booking_id': booking.id,
                'status': booking.get_status_display(),
            })
        else:
            return Response({
                'error': f'Booking {booking_id} cannot be confirmed'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'error': f'Failed to confirm booking: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def booking_search_by_code(request):
    """Search for a booking by confirmation code"""
    try:
        code = request.GET.get('code')
        
        if not code:
            return Response({
                'error': 'code parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        booking = Booking.objects.filter(
            code=code.upper(),
            is_deleted=False
        ).first()
        
        if not booking:
            return Response({
                'error': 'No booking found with this confirmation code'
            }, status=status.HTTP_404_NOT_FOUND)
        
        booking_data = {
            'id': booking.id,
            'code': booking.code,
            'customer_name': booking.customer_name,
            'customer_email': booking.customer_email,
            'customer_phone': booking.customer_phone,
            'table_id': booking.table.id,
            'table_type': booking.table.get_table_type_display(),
            'table_floor': booking.table.floor,
            'booking_date': booking.booking_date.strftime("%Y-%m-%d"),
            'booking_time': booking.booking_time.strftime("%H:%M"),
            'party_size': booking.party_size,
            'duration_hours': float(booking.duration_hours),
            'status': booking.get_status_display(),
            'source': booking.get_source_display(),
            'notes': booking.notes,
            'cancellation_reason': booking.cancellation_reason,
            'created_at': booking.created_at.isoformat(),
            'updated_at': booking.updated_at.isoformat()
        }
        
        return Response(booking_data)
        
    except Exception as e:
        return Response({
            'error': f'Failed to search booking: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
