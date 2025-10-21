import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from typing import Dict, Any, Optional
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class GoogleSheetsService:
    """Service để ghi đơn hàng vào Google Sheets"""
    
    def __init__(self):
        """Initialize Google Sheets service"""
        self.spreadsheet_id = getattr(
            settings,
            'GOOGLE_SHEETS_SPREADSHEET_ID',
            None
        )
        self.worksheet_name = getattr(
            settings,
            'GOOGLE_SHEETS_WORKSHEET_NAME',
            'Orders'
        )
        
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        
        self._initialize()
    
    def _get_credentials_dict(self) -> Optional[Dict[str, Any]]:
        """
        Get credentials dictionary from Django settings
        
        Returns:
            Dictionary containing service account credentials or None
        """
        try:
            credentials_dict = getattr(settings, 'GOOGLE_SERVICE_ACCOUNT', None)
            
            if not credentials_dict:
                logger.warning("GOOGLE_SERVICE_ACCOUNT not configured in settings")
                return None
            
            # Check required fields
            required_fields = ['type', 'project_id', 'private_key', 'client_email']
            for field in required_fields:
                if not credentials_dict.get(field):
                    logger.warning(f"Missing required field in GOOGLE_SERVICE_ACCOUNT: {field}")
                    return None
            
            # Remove None values
            credentials_dict = {k: v for k, v in credentials_dict.items() if v is not None}
            
            return credentials_dict
            
        except Exception as e:
            logger.error(f"Error getting credentials from settings: {e}")
            return None
    
    def _initialize(self):
        """Initialize Google Sheets connection"""
        try:
            if not self.spreadsheet_id:
                logger.warning("GOOGLE_SHEETS_SPREADSHEET_ID not configured")
                return
            
            # Define scope
            scope = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Get credentials from settings
            credentials_dict = self._get_credentials_dict()
            if not credentials_dict:
                logger.warning("Google Sheets credentials not available")
                return
            
            # Create credentials from dictionary
            creds = Credentials.from_service_account_info(
                credentials_dict,
                scopes=scope
            )
            
            # Create client
            self.client = gspread.authorize(creds)
            
            # Open spreadsheet
            self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            
            # Get or create worksheet
            try:
                self.worksheet = self.spreadsheet.worksheet(self.worksheet_name)
            except gspread.exceptions.WorksheetNotFound:
                # Create new worksheet if not exists
                self.worksheet = self.spreadsheet.add_worksheet(
                    title=self.worksheet_name,
                    rows=1000,
                    cols=15
                )
                # Add header row
                self._setup_header()
            
            logger.info("Google Sheets service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets service: {e}")
            self.client = None
    
    def _setup_header(self):
        """Setup header row in worksheet"""
        if not self.worksheet:
            return
        
        headers = [
            'Mã đơn hàng',
            'Ngày đặt',
            'Khách hàng',
            'Số điện thoại',
            'Email',
            'Địa chỉ',
            'Sản phẩm',
            'Size',
            'Màu',
            'Số lượng',
            'Đơn giá',
            'Phí ship',
            'Tổng tiền',
            'Trạng thái',
            'Ghi chú'
        ]
        
        try:
            self.worksheet.update('A1:O1', [headers])
            
            # Format header
            self.worksheet.format('A1:O1', {
                'backgroundColor': {
                    'red': 0.2,
                    'green': 0.2,
                    'blue': 0.8
                },
                'textFormat': {
                    'bold': True,
                    'foregroundColor': {
                        'red': 1.0,
                        'green': 1.0,
                        'blue': 1.0
                    }
                },
                'horizontalAlignment': 'CENTER'
            })
            
            # Freeze header row
            self.worksheet.freeze(rows=1)
            
            logger.info("Header row setup completed")
            
        except Exception as e:
            logger.error(f"Failed to setup header: {e}")
    
    def is_enabled(self) -> bool:
        """Check if Google Sheets integration is enabled"""
        return self.client is not None and self.worksheet is not None
    
    def write_order(self, order_data: Dict[str, Any]) -> bool:
        """
        Ghi đơn hàng vào Google Sheets
        
        Args:
            order_data: Dictionary chứa thông tin đơn hàng
            
        Returns:
            True nếu ghi thành công, False nếu thất bại
        """
        if not self.is_enabled():
            logger.warning("Google Sheets service is not enabled")
            return False
        
        try:
            # Prepare row data
            row = [
                order_data.get('code', ''),
                order_data.get('created_at', datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
                order_data.get('customer_name', ''),
                order_data.get('customer_phone', ''),
                order_data.get('customer_email', ''),
                order_data.get('customer_address', ''),
                order_data.get('product_name', ''),
                order_data.get('product_size', ''),
                order_data.get('product_color', ''),
                str(order_data.get('quantity', 0)),
                f"{order_data.get('price', 0):,.0f}",
                f"{order_data.get('shipping_fee', 0):,.0f}",
                f"{order_data.get('total_amount', 0):,.0f}",
                order_data.get('status', 'PENDING'),
                order_data.get('notes', '')
            ]
            
            # Append row to worksheet
            self.worksheet.append_row(row, value_input_option='USER_ENTERED')
            
            # Highlight new row
            last_row = len(self.worksheet.get_all_values())
            self._highlight_new_row(last_row)
            
            logger.info(f"Order {order_data.get('code')} written to Google Sheets successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write order to Google Sheets: {e}")
            return False
    
    def _highlight_new_row(self, row_number: int):
        """Highlight newly added row"""
        try:
            self.worksheet.format(f'A{row_number}:O{row_number}', {
                'backgroundColor': {
                    'red': 0.9,
                    'green': 1.0,
                    'blue': 0.9
                }
            })
        except Exception as e:
            logger.error(f"Failed to highlight row: {e}")
    
    def write_order_batch(self, orders: list) -> int:
        """
        Ghi nhiều đơn hàng cùng lúc
        
        Args:
            orders: List of order dictionaries
            
        Returns:
            Number of successfully written orders
        """
        if not self.is_enabled():
            return 0
        
        success_count = 0
        for order in orders:
            if self.write_order(order):
                success_count += 1
        
        return success_count
    
    def update_order_status(self, order_code: str, new_status: str) -> bool:
        """
        Cập nhật trạng thái đơn hàng
        
        Args:
            order_code: Mã đơn hàng
            new_status: Trạng thái mới
            
        Returns:
            True nếu cập nhật thành công
        """
        if not self.is_enabled():
            return False
        
        try:
            # Find row with order_code
            cell = self.worksheet.find(order_code)
            if cell:
                # Update status column (column N = 14)
                self.worksheet.update_cell(cell.row, 14, new_status)
                logger.info(f"Updated status for order {order_code} to {new_status}")
                return True
            else:
                logger.warning(f"Order {order_code} not found in sheet")
                return False
                
        except Exception as e:
            logger.error(f"Failed to update order status: {e}")
            return False
    
    def get_all_orders(self) -> list:
        """
        Lấy tất cả đơn hàng từ sheet
        
        Returns:
            List of order dictionaries
        """
        if not self.is_enabled():
            return []
        
        try:
            records = self.worksheet.get_all_records()
            return records
        except Exception as e:
            logger.error(f"Failed to get orders: {e}")
            return []
    
    def test_connection(self) -> str:
        """
        Test connection to Google Sheets
        
        Returns:
            Status message
        """
        if not self.is_enabled():
            return "❌ Google Sheets service is not enabled"
        
        try:
            # Try to read first cell
            value = self.worksheet.acell('A1').value
            return f"✅ Connected successfully! First cell: {value}"
        except Exception as e:
            return f"❌ Connection failed: {e}"
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Lấy thống kê từ sheet
        
        Returns:
            Dictionary with statistics
        """
        if not self.is_enabled():
            return {}
        
        try:
            orders = self.get_all_orders()
            
            total_orders = len(orders)
            total_revenue = sum(
                float(order.get('Tổng tiền', '0').replace(',', ''))
                for order in orders
            )
            
            # Count by status
            status_counts = {}
            for order in orders:
                status = order.get('Trạng thái', 'UNKNOWN')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            return {
                'total_orders': total_orders,
                'total_revenue': total_revenue,
                'status_counts': status_counts
            }
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {}


# Global instance
_google_sheets_service = None


def get_google_sheets_service() -> Optional[GoogleSheetsService]:
    """Get singleton instance of GoogleSheetsService"""
    global _google_sheets_service
    
    if _google_sheets_service is None:
        _google_sheets_service = GoogleSheetsService()
    
    return _google_sheets_service if _google_sheets_service.is_enabled() else None
