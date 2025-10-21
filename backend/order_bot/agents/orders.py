from langchain.tools import tool
from order_bot.models.order import Order, OrderItem
from order_bot.models.product import Product
from typing import Optional
from django.db import transaction
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class OrdersService:
    """Service to handle order operations for fashion shop"""
    
    @staticmethod
    @tool
    def create_order(
        customer_name: str,
        customer_phone: str,
        customer_address: str,
        product_id: int,
        quantity: int = 1,
        customer_email: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> str:
        """
        Tạo đơn hàng mới cho khách hàng.
        
        Args:
            customer_name: Tên khách hàng
            customer_phone: Số điện thoại khách hàng
            customer_address: Địa chỉ giao hàng
            product_id: ID sản phẩm
            quantity: Số lượng (mặc định 1)
            customer_email: Email khách hàng (tùy chọn)
            notes: Ghi chú đơn hàng (tùy chọn)
        
        Returns:
            Thông tin đơn hàng đã tạo hoặc thông báo lỗi
        """
        try:
            with transaction.atomic():
                # Get product
                product = Product.objects.select_for_update().get(
                    id=product_id,
                    is_active=True
                )
                
                # Check stock
                if product.stock < quantity:
                    return f"Sản phẩm {product.name} chỉ còn {product.stock} sản phẩm, không đủ số lượng {quantity}."
                
                # Create order
                order = Order.objects.create(
                    customer_name=customer_name,
                    customer_phone=customer_phone,
                    customer_email=customer_email,
                    customer_address=customer_address,
                    notes=notes,
                    status=Order.OrderStatus.PENDING,
                    payment_method=Order.PaymentMethod.COD,
                    shipping_fee=Decimal('30000'),  # Default shipping fee
                )
                
                # Create order item
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.final_price,
                )
                
                # Update product stock
                product.stock -= quantity
                product.save()
                
                # Write to Google Sheets (if enabled)
                try:
                    from order_bot.services.google_sheets_service import get_google_sheets_service
                    
                    sheets_service = get_google_sheets_service()
                    if sheets_service:
                        order_item = OrderItem.objects.filter(order=order).first()
                        sheets_data = {
                            'code': order.code,
                            'created_at': order.created_at,
                            'customer_name': order.customer_name,
                            'customer_phone': order.customer_phone,
                            'customer_email': order.customer_email or '',
                            'customer_address': order.customer_address,
                            'product_name': product.name,
                            'product_size': product.get_size_display(),
                            'product_color': product.get_color_display(),
                            'quantity': quantity,
                            'price': product.final_price,
                            'shipping_fee': order.shipping_fee,
                            'total_amount': order.total_amount,
                            'status': order.get_status_display(),
                            'notes': order.notes or ''
                        }
                        
                        if sheets_service.write_order(sheets_data):
                            logger.info(f"Order {order.code} written to Google Sheets")
                        else:
                            logger.warning(f"Failed to write order {order.code} to Google Sheets")
                except Exception as e:
                    logger.error(f"Error writing to Google Sheets: {e}")
                    # Don't fail the order creation if Sheets write fails
                
                result = f"Đơn hàng đã được tạo thành công!\n\n"
                result += f"Mã đơn hàng: {order.code}\n"
                result += f"Khách hàng: {order.customer_name}\n"
                result += f"Số điện thoại: {order.customer_phone}\n"
                result += f"Địa chỉ: {order.customer_address}\n"
                result += f"Sản phẩm: {product.name} x {quantity}\n"
                result += f"Tổng tiền hàng: {order.subtotal:,.0f} VNĐ\n"
                result += f"Phí vận chuyển: {order.shipping_fee:,.0f} VNĐ\n"
                result += f"Tổng thanh toán: {order.total_amount:,.0f} VNĐ\n"
                result += f"Trạng thái: Chờ xác nhận\n"
                
                return result
                
        except Product.DoesNotExist:
            return f"Không tìm thấy sản phẩm với ID {product_id}"
        except Exception as e:
            return f"Có lỗi xảy ra khi tạo đơn hàng: {str(e)}"
    
    @staticmethod
    @tool
    def summary_order_info(
        customer_name: str,
        customer_phone: str,
        customer_address: str,
        product_id: int,
        quantity: int = 1,
        customer_email: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> str:
        """
        Tóm tắt thông tin đơn hàng trước khi xác nhận.
        
        Args:
            customer_name: Tên khách hàng
            customer_phone: Số điện thoại khách hàng
            customer_address: Địa chỉ giao hàng
            product_id: ID sản phẩm
            quantity: Số lượng (mặc định 1)
            customer_email: Email khách hàng (tùy chọn)
            notes: Ghi chú đơn hàng (tùy chọn)
        
        Returns:
            Tóm tắt thông tin đơn hàng
        """
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            
            subtotal = product.final_price * quantity
            shipping_fee = Decimal('30000')
            total = subtotal + shipping_fee
            
            result = "=== THÔNG TIN ĐƠN HÀNG ===\n\n"
            result += f"Khách hàng: {customer_name}\n"
            result += f"Số điện thoại: {customer_phone}\n"
            if customer_email:
                result += f"Email: {customer_email}\n"
            result += f"Địa chỉ giao hàng: {customer_address}\n\n"
            
            result += f"Sản phẩm: {product.name}\n"
            result += f"Size: {product.get_size_display()}\n"
            result += f"Màu: {product.get_color_display()}\n"
            result += f"Số lượng: {quantity}\n"
            result += f"Đơn giá: {product.final_price:,.0f} VNĐ\n\n"
            
            result += f"Tổng tiền hàng: {subtotal:,.0f} VNĐ\n"
            result += f"Phí vận chuyển: {shipping_fee:,.0f} VNĐ\n"
            result += f"Tổng thanh toán: {total:,.0f} VNĐ\n\n"
            
            if notes:
                result += f"Ghi chú: {notes}\n\n"
            
            result += "Phương thức thanh toán: Thanh toán khi nhận hàng (COD)\n"
            result += "Thời gian giao hàng dự kiến: 2-3 ngày\n"
            
            return result
            
        except Product.DoesNotExist:
            return f"Không tìm thấy sản phẩm với ID {product_id}"
    
    @staticmethod
    @tool
    def get_order_detail(order_code: str) -> str:
        """
        Lấy thông tin chi tiết đơn hàng theo mã.
        
        Args:
            order_code: Mã đơn hàng
        
        Returns:
            Thông tin chi tiết đơn hàng
        """
        try:
            order = Order.objects.get(code=order_code)
            
            result = f"=== THÔNG TIN ĐƠN HÀNG {order.code} ===\n\n"
            result += f"Khách hàng: {order.customer_name}\n"
            result += f"Số điện thoại: {order.customer_phone}\n"
            if order.customer_email:
                result += f"Email: {order.customer_email}\n"
            result += f"Địa chỉ: {order.customer_address}\n\n"
            
            result += "Sản phẩm:\n"
            for item in order.items.all():
                result += f"- {item.product_name} ({item.product_size}, {item.product_color}) x {item.quantity}\n"
                result += f"  Giá: {item.price:,.0f} VNĐ\n"
            
            result += f"\nTổng tiền hàng: {order.subtotal:,.0f} VNĐ\n"
            result += f"Phí vận chuyển: {order.shipping_fee:,.0f} VNĐ\n"
            result += f"Tổng thanh toán: {order.total_amount:,.0f} VNĐ\n\n"
            
            result += f"Trạng thái: {order.get_status_display()}\n"
            result += f"Phương thức thanh toán: {order.get_payment_method_display()}\n"
            result += f"Ngày đặt: {order.created_at.strftime('%d/%m/%Y %H:%M')}\n"
            
            if order.notes:
                result += f"\nGhi chú: {order.notes}\n"
            
            return result
            
        except Order.DoesNotExist:
            return f"Không tìm thấy đơn hàng với mã {order_code}"
    
    def create_tools(self):
        """Create list of tools for the agent"""
        return [
            self.create_order,
            self.summary_order_info,
            self.get_order_detail,
        ]
