from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from restaurant_booking.models.table import Table

class TableIdInput(BaseModel):
    table_id: int = Field(..., description="ID của bàn")

class TableSearchInput(BaseModel):
    booking_date: Optional[str] = None
    booking_time: Optional[str] = None
    table_type: Optional[str] = None
    party_size: int = None
    floor: int = None

class GuestInformation(BaseModel):
    guest_name: Optional[str] = None
    guest_phone: Optional[str] = None
    note: Optional[str] = None

class BookingEntity(TableSearchInput, GuestInformation):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    table_id: Optional[int] = None

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
