from typing import Optional, List, Any
from restaurant_booking.agents.io_models.input import (
    TableSearchInput,
    TableIdInput,
    BookingEntity,
)
from restaurant_booking.models import Table, Booking
from datetime import datetime
from langchain_core.tools import StructuredTool
from datetime import datetime


class TablesService:

    def _search_tables(
        self,
        booking_date: str = None,
        booking_time: str = None,
        table_type: str = None,
        party_size: int = None,
        floor: int = None,
        table_id: Optional[int] = None,
    ) -> str:
        """
        Tìm kiếm các bàn trống phù hợp với yêu cầu đặt bàn.
        """
        try:
            error = self.validate_search_tables_info(booking_date, booking_time, table_type, party_size, floor)
            if error:
                return error

            tables = Table.objects.filter(
                is_deleted=False,
                capacity__gte=party_size,
                table_type=table_type,
                floor=floor,
            )

            if table_id:
                tables = tables.filter(id=table_id)

            date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
            booking_time_obj = datetime.strptime(booking_time, "%H:%M").time()
            booked_tables = Booking.objects.filter(
                booking_date=date_obj,
                # booking_time__gte=booking_time_obj,
                # booking_time__lte=booking_time_obj + timedelta(hours=2),
                status__in=[
                    Booking.BookingStatus.CONFIRMED,
                    Booking.BookingStatus.PENDING,
                ],
            ).values_list("table_id", flat=True)

            available_tables = tables.exclude(id__in=booked_tables)

            # Prepare result
            result = []
            for table in available_tables:
                result.append(
                    {
                        "table_id": table.id,
                        "table_type": table.get_table_type_display(),
                        "capacity": table.capacity,
                        "floor": table.floor,
                        "status": table.get_status_display(),
                        "notes": table.notes or "",
                    }
                )

            if not result:
                return "Không tìm thấy bàn phù hợp với yêu cầu của bạn."

            return result

        except Exception as e:
            return f"Lỗi khi tìm kiếm bàn: {str(e)}"

    def _get_table_by_id(self, table_id: int) -> str:
        """
        Lấy thông tin bàn theo ID.
        """
        try:
            table = Table.objects.get(id=table_id)
            result = f"""
            Thông tin bàn:
            Số: {table.id}
            Loại bàn: {table.get_table_type_display()}
            Sức chứa: {table.capacity}
            Chiều rộng: {table.width}
            Chiều dài: {table.length}
            Tầng: {table.floor}
            """
            return result
        except Exception as e:
            return f"Lỗi khi lấy thông tin bàn: {str(e)}"

    def _book_table(
        self,
        table_id: int,
        booking_date: str,
        booking_time: str,
        party_size: int,
        table_type: str,
        floor: int,
        guest_name: str,
        guest_phone: str,
        note: str = "",
    ) -> str:
        """
        Đặt bàn.
        """
        try:
            error = self.validate_guest_info(guest_name, guest_phone, note)
            if error:
                return error

            table = Table.objects.filter(
                id=table_id,
                status=Table.TableStatus.AVAILABLE,
            )
            if not table:
                return "Không tìm thấy bàn phù hợp với yêu cầu của bạn. Vui lòng thử lại với thông tin khác."

            table = table.first()

            booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
            booking_time_obj = datetime.strptime(booking_time, "%H:%M").time()

            # booking_data = BookingEntity(
            #     table_id=table_id,
            #     booking_date=booking_date,
            #     booking_time=booking_time,
            #     party_size=party_size,
            #     guest_name=guest_name,
            #     guest_phone=guest_phone,
            #     note=note,
            # )

            # booking_data_dict = booking_data.model_dump()

            booking = Booking.objects.create(
                table_id=table_id,
                guest_name=guest_name,
                guest_phone=guest_phone,
                booking_date=booking_date_obj,
                booking_time=booking_time_obj,
                party_size=party_size,
                notes=note,
                status=Booking.BookingStatus.CONFIRMED,
                source=Booking.BookingSource.WEBSITE,
                duration_hours=2.0,
            )

        except Exception as e:
            return f"Lỗi khi đặt bàn: {str(e)}"

        return f"Đã đặt bàn thành công. Mã đặt bàn: {booking.code}. Bạn có thể tra cứu thông tin đặt bàn tại đây: http://chatai.pscds.com/restaurant-booking/search?code={booking.code}"

    def _summary_booking_info(
        self, 
        table_id: int = None,
        booking_date: str = None,
        booking_time: str = None,
        party_size: int = None,
        table_type: str = None,
        floor: int = None,
        guest_name: str = None,
        guest_phone: str = None,
        note: str = None
    ) -> str:
        """
        Summary booking information.
        """
        return f"""Em xin xác nhận lại thông tin đặt bàn:
        Thông tin đặt bàn:
        Bàn số: {table_id}
        Ngày đặt bàn: {booking_date}
        Giờ đặt bàn: {booking_time}
        Số lượng người: {party_size}
        Loại bàn: {table_type}
        Tầng: {floor}
        Tên khách: {guest_name}
        Số điện thoại: {guest_phone}
        Ghi chú: {note}
        Anh/chị vui lòng xác nhận thông tin trên đã đúng chưa ạ?
        """

    def validate_guest_info(self, guest_name: str, guest_phone: str, note: str = None) -> str:
        """
        Validate guest information.
        """
        if not guest_name or not guest_phone:
            return f"Hỏi thông tin: guest_name và guest_phone của khách hàng."
        if note is None:
            return f"Hỏi thông tin: note của khách hàng."
        return None

    def validate_search_tables_info(self, booking_date: str, booking_time: str, table_type: str, party_size: int, floor: int) -> str:
        """
        Validate table information.
        """
        if not booking_date and not booking_time:
            return f"Hỏi thông tin: booking_date và booking_time của khách hàng."
        if not booking_date:
            return f"Hỏi thông tin: booking_date của khách hàng."
        if not booking_time:
            return f"Hỏi thông tin: booking_time của khách hàng."
        if not table_type:
            return f"Hỏi thông tin: table_type của khách hàng."
        if not party_size:
            return f"Hỏi thông tin: party_size của khách hàng."
        if not floor:
            return f"Hỏi thông tin: floor của khách hàng."
        return None

    def create_tools(self) -> List[Any]:
        return [
            StructuredTool.from_function(
                func=self._search_tables,
                name="search_tables",
                description=(
                    """Tìm kiếm các bàn trống phù hợp với yêu cầu đặt bàn.
                    Nhận vào: 
                    booking_date: Ngày đặt bàn (YYYY-MM-DD),
                    booking_time: Giờ đặt bàn (HH:MM), 
                    table_type: Loại bàn,
                    party_size: Số người, 
                    floor: Tầng, 
                    table_id: ID bàn (tùy chọn).
                    Trả về danh sách bàn phù hợp hoặc thông báo nếu không có bàn.
                    Chỉ được gọi khi tất cả tham số đã được cung cấp rõ ràng từ người dùng. Không được tự suy đoán hoặc sử dụng giá trị mặc định
                    """
                ),
                args_schema=TableSearchInput,
            ),
            StructuredTool.from_function(
                func=self._book_table,
                name="book_table",
                description=(
                    """Đặt bàn.
                    Nhận vào: 
                    table_id (ID của bàn),
                    booking_date (YYYY-MM-DD), 
                    booking_time (HH:MM), 
                    party_size (số lượng người), 
                    guest_name (tên khách hàng), 
                    guest_phone (số điện thoại khách hàng),
                    note (ghi chú của khách hàng).
                    Trả về thông báo thành công hoặc thông báo lỗi.
                    """
                ),
                args_schema=BookingEntity,
            ),
            StructuredTool.from_function(
                func=self._get_table_by_id,
                name="get_table_by_id",
                description=(
                    """Lấy thông tin bàn theo ID.
                    Nhận vào: table_id (ID của bàn).
                    Trả về thông tin bàn.
                    """
                ),
                args_schema=TableIdInput,
            ),
            StructuredTool.from_function(
                func=self._summary_booking_info,
                name="summary_booking_info",
                description=(
                    """Tóm tắt thông tin đặt bàn và yêu cầu xác nhận.
                    Nhận vào: table_id (ID của bàn),
                    booking_date (YYYY-MM-DD),
                    booking_time (HH:MM),
                    party_size (số lượng người),
                    table_type (loại bàn),
                    floor (tầng),
                    guest_name (tên khách hàng),
                    guest_phone (số điện thoại khách hàng),
                    note (ghi chú của khách hàng).
                    Trả về thông tin đặt bàn và yêu cầu xác nhận.
                    """
                ),
                args_schema=BookingEntity,
            ),
        ]
