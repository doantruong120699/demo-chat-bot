from typing import Optional, List, Any
from restaurant_booking.agents.io_models.input import TableSearchInput, NaturalTimeInput, BookingEntity
from restaurant_booking.models import Table, Booking
from datetime import datetime, timedelta
from langchain_core.tools import StructuredTool, Tool
import re
import json
from datetime import datetime

class TablesService:
    def _search_tables(
        self,
        party_size: Optional[int] = None,
        booking_date: Optional[str] = None,
        booking_time: Optional[str] = None,
        table_type: Optional[str] = None,
        floor: Optional[int] = None,
        table_id: Optional[int] = None,
    ) -> str:
        """
        Tìm kiếm các bàn trống phù hợp với yêu cầu đặt bàn.
        """
        try:
            # Kiểm tra thông tin bắt buộc trước khi tìm kiếm
            missing_info = []
            
            if not booking_date:
                missing_info.append("ngày đặt bàn")
            if not party_size:
                missing_info.append("số lượng khách")
            
            if missing_info:
                return f"Để tìm kiếm bàn, PSCD cần thông tin: {', '.join(missing_info)}. Bạn có thể cung cấp thông tin này không?"
            
            # Parse booking_date
            try:
                date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
            except Exception:
                return "Không tìm thấy bàn: Ngày đặt không hợp lệ."

            # Base queryset
            tables = Table.objects.filter(is_deleted=False, capacity__gte=party_size)

            if table_type:
                tables = tables.filter(table_type=table_type)
            if floor:
                tables = tables.filter(floor=floor)
            if table_id:
                tables = tables.filter(id=table_id)
            # Filter out tables that are booked at the given date (and time if provided)
            booked_tables = Booking.objects.filter(
                booking_date=date_obj,
                status__in=[
                    Booking.BookingStatus.CONFIRMED,
                    Booking.BookingStatus.PENDING,
                ],
            ).values_list("table_id", flat=True)

            # if booking_time:
            #     try:
            #         booking_time_obj = dt.strptime(booking_time, "%H:%M").time()
            #         print(booking_time_obj)
            #     except Exception:
            #         return "Không tìm thấy bàn: Giờ đặt không hợp lệ."
            #     tables = tables.filter(bookings__booking_time=booking_time_obj)

            available_tables = tables.exclude(id__in=booked_tables)

            # Prepare result
            result = []
            for table in available_tables:
                result.append(
                    {
                        "id": table.id,
                        "table_type": table.get_table_type_display(),
                        "capacity": table.capacity,
                        "floor": table.floor,
                        "status": table.get_status_display(),
                        "notes": table.notes or "",
                    }
                )

            if not result:
                return "Không tìm thấy bàn phù hợp với yêu cầu của bạn."

            return json.dumps(result, ensure_ascii=False)

        except Exception as e:
            return f"Lỗi khi tìm kiếm bàn: {str(e)}"

    def _book_table(
        self,
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
            table = Table.objects.filter(status=Table.TableStatus.AVAILABLE, capacity__gte=party_size, table_type=table_type, floor=floor)
            if not table:
                return "Không tìm thấy bàn phù hợp với yêu cầu của bạn. Vui lòng thử lại với thông tin khác."

            table = table.first()

            booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
            booking_time_obj = datetime.strptime(booking_time, "%H:%M").time()

            booking_data = BookingEntity(
                booking_date=booking_date_obj,
                booking_time=booking_time_obj,
                party_size=party_size,
                table=table,
                table_type=table_type,
                floor=floor,
                guest_name=guest_name,
                guest_phone=guest_phone,
                note=note,
            )

            booking_data = booking_data.model_dump()
            
            booking = Booking.objects.create(
                **booking_data,
                status=Booking.BookingStatus.CONFIRMED,
                source=Booking.BookingSource.WEBSITE,
                duration_hours=2.0,
            )

        except Exception as e:
            return f"Lỗi khi đặt bàn: {str(e)}"

        return f"Đã đặt bàn thành công. Mã đặt bàn: {booking.code}"

    def _get_current_datetime(self) -> str:
        """
        Lấy thời gian hiện tại của hệ thống.
        """
        try:
            now = datetime.now()
            return json.dumps(
                {
                    "current_date": now.strftime("%Y-%m-%d"),
                    "current_time": now.strftime("%H:%M"),
                    "current_datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
                    "weekday": now.strftime("%A"),
                    "weekday_vietnamese": self._get_vietnamese_weekday(now.weekday()),
                },
                ensure_ascii=False,
            )
        except Exception as e:
            return f"Lỗi khi lấy thời gian hiện tại: {str(e)}"

    def _get_vietnamese_weekday(self, weekday: int) -> str:
        """Chuyển đổi thứ từ số sang tiếng Việt"""
        weekdays = [
            "thứ hai",
            "thứ ba",
            "thứ tư",
            "thứ năm",
            "thứ sáu",
            "thứ bảy",
            "chủ nhật",
        ]
        return weekdays[weekday]

    def _parse_natural_time(self, natural_time: str) -> str:
        """
        Chuyển đổi thời gian tự nhiên sang định dạng chuẩn.
        """
        try:
            now = datetime.now()
            natural_time = natural_time.lower().strip()

            # Xử lý các trường hợp đặc biệt
            if natural_time in ["hôm nay", "ngày hôm nay"]:
                date = now.strftime("%Y-%m-%d")
                return json.dumps(
                    {
                        "date": date,
                        # "time": time,
                        # "datetime": f"{date} {time}",
                        "original": natural_time,
                    },
                    ensure_ascii=False,
                )

            elif natural_time in ["mai", "ngày mai"]:
                tomorrow = now + timedelta(days=1)
                date = tomorrow.strftime("%Y-%m-%d")
                return json.dumps(
                    {
                        "date": date,
                        # "time": time,
                        # "datetime": f"{date} {time}",
                        "original": natural_time,
                    },
                    ensure_ascii=False,
                )

            elif natural_time in ["ngày kia"]:
                day_after = now + timedelta(days=2)
                date = day_after.strftime("%Y-%m-%d")
                return json.dumps(
                    {
                        "date": date,
                        # "time": time,
                        # "datetime": f"{date} {time}",
                        "original": natural_time,
                    },
                    ensure_ascii=False,
                )

            elif natural_time in ["tối nay", "tối nay"]:
                date = now.strftime("%Y-%m-%d")
                return json.dumps(
                    {
                        "date": date,
                        # "time": time,
                        # "datetime": f"{date} {time}",
                        "original": natural_time,
                    },
                    ensure_ascii=False,
                )

            elif natural_time in ["sáng nay", "sáng nay"]:
                date = now.strftime("%Y-%m-%d")
                return json.dumps(
                    {
                        "date": date,
                        # "time": time,
                        # "datetime": f"{date} {time}",
                        "original": natural_time,
                    },
                    ensure_ascii=False,
                )

            elif natural_time in ["trưa nay", "trưa nay"]:
                date = now.strftime("%Y-%m-%d")
                return json.dumps(
                    {
                        "date": date,
                        # "time": time,
                        # "datetime": f"{date} {time}",
                        "original": natural_time,
                    },
                    ensure_ascii=False,
                )

            elif natural_time in ["chiều nay", "chiều nay"]:
                date = now.strftime("%Y-%m-%d")
                return json.dumps(
                    {
                        "date": date,
                        # "time": time,
                        # "datetime": f"{date} {time}",
                        "original": natural_time,
                    },
                    ensure_ascii=False,
                )

            # Xử lý thứ trong tuần
            elif "thứ" in natural_time:
                target_weekday = self._parse_weekday(natural_time)
                if target_weekday is not None:
                    days_ahead = target_weekday - now.weekday()
                    if days_ahead <= 0:  # Nếu thứ đó đã qua trong tuần này
                        days_ahead += 7  # Chuyển sang tuần sau

                    target_date = now + timedelta(days=days_ahead)
                    date = target_date.strftime("%Y-%m-%d")
                    return json.dumps(
                        {
                            "date": date,
                            # "time": time,
                            # "datetime": f"{date} {time}",
                            "original": natural_time,
                        },
                        ensure_ascii=False,
                    )

            # Xử lý cuối tuần
            elif natural_time in ["cuối tuần", "cuối tuần này", "cuối tuần này"]:
                # Tìm thứ bảy gần nhất
                days_until_saturday = (5 - now.weekday()) % 7
                if days_until_saturday == 0 and now.weekday() == 5:
                    days_until_saturday = (
                        7  # Nếu hôm nay là thứ bảy, lấy thứ bảy tuần sau
                    )
                elif days_until_saturday == 0:
                    days_until_saturday = 7

                saturday = now + timedelta(days=days_until_saturday)
                date = saturday.strftime("%Y-%m-%d")
                return json.dumps(
                    {
                        "date": date,
                        # "time": time,
                        # "datetime": f"{date} {time}",
                        "original": natural_time,
                    },
                    ensure_ascii=False,
                )

            # Xử lý thời gian với giờ cụ thể
            time_pattern = r"(\d{1,2}):(\d{2})"
            time_match = re.search(time_pattern, natural_time)
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2))
                time_str = f"{hour:02d}:{minute:02d}"

                # Xác định ngày
                if "mai" in natural_time or "ngày mai" in natural_time:
                    target_date = now + timedelta(days=1)
                elif "hôm nay" in natural_time or "nay" in natural_time:
                    target_date = now
                else:
                    target_date = now

                date = target_date.strftime("%Y-%m-%d")
                return json.dumps(
                    {
                        "date": date,
                        # "time": time_str,
                        # "datetime": f"{date} {time_str}",
                        "original": natural_time,
                    },
                    ensure_ascii=False,
                )

            # Nếu không nhận diện được, trả về thời gian hiện tại
            return json.dumps(
                {
                    "date": now.strftime("%Y-%m-%d"),
                    # "time": now.strftime("%H:%M"),
                    # "datetime": f"{now.strftime('%Y-%m-%d')} {now.strftime('%H:%M')}",
                    "original": natural_time,
                    "note": "Không nhận diện được thời gian, sử dụng thời gian hiện tại",
                },
                ensure_ascii=False,
            )

        except Exception as e:
            return f"Lỗi khi chuyển đổi thời gian: {str(e)}"

    def _parse_weekday(self, text: str) -> Optional[int]:
        """Chuyển đổi thứ từ tiếng Việt sang số (0=thứ hai, 6=chủ nhật)"""
        weekday_map = {
            "thứ hai": 0,
            "thứ 2": 0,
            "t2": 0,
            "thứ ba": 1,
            "thứ 3": 1,
            "t3": 1,
            "thứ tư": 2,
            "thứ 4": 2,
            "t4": 2,
            "thứ năm": 3,
            "thứ 5": 3,
            "t5": 3,
            "thứ sáu": 4,
            "thứ 6": 4,
            "t6": 4,
            "thứ bảy": 5,
            "thứ 7": 5,
            "t7": 5,
            "chủ nhật": 6,
            "cn": 6,
        }

        for key, value in weekday_map.items():
            if key in text.lower():
                return value
        return None

    def create_tools(self) -> List[Any]:
        return [
            StructuredTool.from_function(
                func=self._search_tables,
                name="search_tables",
                description=(
                    """Tìm kiếm các bàn trống phù hợp với yêu cầu đặt bàn.
                    Nhận vào: party_size (số người), booking_date (YYYY-MM-DD), 
                    booking_time (tùy chọn, HH:MM), table_type (tùy chọn), floor (tùy chọn),
                    Trả về danh sách bàn phù hợp hoặc thông báo nếu không có bàn.
                    """
                ),
                args_schema=TableSearchInput,
            ),
            StructuredTool.from_function(
                func=self._get_current_datetime,
                name="get_current_datetime",
                description=(
                    """Lấy thời gian hiện tại của hệ thống.
                    Trả về thông tin ngày giờ hiện tại, thứ trong tuần bằng tiếng Việt.
                    """
                ),
            ),
            StructuredTool.from_function(
                func=self._parse_natural_time,
                name="parse_natural_time",
                description=(
                    """Chuyển đổi thời gian tự nhiên sang định dạng chuẩn ISO.
                    Hỗ trợ các từ khóa: 'hôm nay', 'mai', 'ngày kia', 'tối nay', 'sáng nay', 
                    'trưa nay', 'chiều nay', 'thứ bảy', 'thứ hai', 'cuối tuần', v.v.
                    Trả về JSON với date (YYYY-MM-DD), time (HH:MM), datetime (YYYY-MM-DD HH:MM).
                    """
                ),
                args_schema=NaturalTimeInput,
            ),
            StructuredTool.from_function(
                func=self._book_table,
                name="book_table",
                description=(
                    """Đặt bàn.
                    Nhận vào: 
                    booking_date (YYYY-MM-DD), 
                    booking_time (HH:MM), 
                    table_type (loại bàn),
                    floor (tầng),
                    party_size (số lượng người), 
                    guest_name (tên khách hàng), 
                    guest_phone (số điện thoại khách hàng),
                    note (ghi chú của khách hàng).
                    Trả về thông báo thành công hoặc thông báo lỗi.
                    """
                ),
                args_schema=BookingEntity,
            ),
        ]
