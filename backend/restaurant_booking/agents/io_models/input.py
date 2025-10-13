from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from restaurant_booking.models.table import Table


class TableSearchInput(BaseModel):
    booking_date: Optional[str] = Field(None, description="Ngày đặt bàn (YYYY-MM-DD)")
    booking_time: Optional[str] = Field(None, description="Giờ đặt bàn (HH:MM)")
    table_type: Optional[str] = Field(
        None,
        description=(
            "Loại bàn, lựa chọn từ các loại bàn sau: "
            + ", ".join([f"{c.name} ({c.label})" for c in Table.TableType])
        ),
    )
    party_size: Optional[int] = Field(None, description="Số lượng người muốn đặt bàn")
    floor: Optional[int] = Field(None, description="Tầng")

class GuestInformation(BaseModel):
    guest_name: Optional[str] = Field(None, description="Tên khách hàng")
    guest_phone: Optional[str] = Field(None, description="Số điện thoại khách hàng")
    note: Optional[str] = Field(None, description="Ghi chú khách hàng")

class BookingEntity(TableSearchInput, GuestInformation):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    table_id: Optional[int] = Field(None, description="ID của bàn liên kết với đặt bàn (nếu có)")

    def model_dump(self):
        """Convert to dictionary for memory storage"""
        fields = [
            'booking_date',
            'booking_time', 
            'table_type',
            'party_size',
            'guest_name',
            'guest_phone',
            'note',
            'floor',
            'table_id',
        ]
        return {field: getattr(self, field, None) for field in fields}

class NaturalTimeInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    natural_time: str = Field(
        ...,
        description="Thời gian tự nhiên cần chuyển đổi (ví dụ: 'hôm nay', 'mai', 'tối nay', 'thứ bảy')",
    )
