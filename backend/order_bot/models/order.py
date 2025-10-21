from django.db import models
from django.core.validators import MinValueValidator
from common.models.base import DateTimeModel, SoftDeleteModel
import random
import string


class Order(DateTimeModel, SoftDeleteModel):
    """
    Order model for fashion shop orders
    """
    
    class OrderStatus(models.TextChoices):
        PENDING = "PENDING", "Chờ xác nhận"
        CONFIRMED = "CONFIRMED", "Đã xác nhận"
        PROCESSING = "PROCESSING", "Đang xử lý"
        SHIPPING = "SHIPPING", "Đang giao hàng"
        DELIVERED = "DELIVERED", "Đã giao hàng"
        COMPLETED = "COMPLETED", "Hoàn thành"
        CANCELLED = "CANCELLED", "Đã hủy"
        RETURNED = "RETURNED", "Đã hoàn trả"
    
    class PaymentMethod(models.TextChoices):
        COD = "COD", "Thanh toán khi nhận hàng"
        BANK_TRANSFER = "BANK_TRANSFER", "Chuyển khoản ngân hàng"
        CREDIT_CARD = "CREDIT_CARD", "Thẻ tín dụng"
        MOMO = "MOMO", "Ví MoMo"
        ZALOPAY = "ZALOPAY", "ZaloPay"
        VNPAY = "VNPAY", "VNPay"
    
    # Order code
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã đơn hàng",
        editable=False
    )
    
    # Customer information
    customer_name = models.CharField(
        max_length=100,
        verbose_name="Tên khách hàng"
    )
    customer_phone = models.CharField(
        max_length=20,
        verbose_name="Số điện thoại"
    )
    customer_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email"
    )
    customer_address = models.CharField(
        max_length=255,
        verbose_name="Địa chỉ giao hàng"
    )
    
    # Order status
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name="Trạng thái"
    )
    
    # Payment
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.COD,
        verbose_name="Phương thức thanh toán"
    )
    payment_status = models.BooleanField(
        default=False,
        verbose_name="Đã thanh toán"
    )
    
    # Pricing
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Tổng tiền hàng"
    )
    shipping_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Phí vận chuyển"
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Số tiền giảm giá"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Tổng thanh toán"
    )
    
    # Notes
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Ghi chú"
    )
    
    # Cancellation
    cancellation_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name="Lý do hủy"
    )
    
    # Delivery tracking
    delivery_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Ngày giao hàng"
    )
    tracking_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Mã vận đơn"
    )

    class Meta:
        db_table = 'fashion_orders'
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['customer_phone']),
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self):
        return f"Order #{self.code} - {self.customer_name}"

    def save(self, *args, **kwargs):
        # Generate unique order code if not exists
        if not self.code:
            self.code = self._generate_unique_code()
        
        # Calculate total amount
        self.total_amount = self.subtotal + self.shipping_fee - self.discount_amount
        
        super().save(*args, **kwargs)

    def _generate_unique_code(self, length=8):
        """Generate a unique order code"""
        while True:
            code = 'ORD' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            if not Order.objects.filter(code=code).exists():
                return code
    
    @property
    def calc_total_amount(self):
        """Calculate total from order items"""
        return sum(item.subtotal for item in self.items.all())


class OrderItem(DateTimeModel):
    """
    Order item model for products in an order
    """
    
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name="Đơn hàng"
    )
    product = models.ForeignKey(
        'order_bot.Product',
        on_delete=models.CASCADE,
        verbose_name="Sản phẩm"
    )
    
    # Product details at time of order (snapshot)
    product_name = models.CharField(
        max_length=200,
        verbose_name="Tên sản phẩm"
    )
    product_size = models.CharField(
        max_length=20,
        verbose_name="Kích cỡ"
    )
    product_color = models.CharField(
        max_length=20,
        verbose_name="Màu sắc"
    )
    
    # Quantity and pricing
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Số lượng"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Đơn giá"
    )
    
    class Meta:
        db_table = 'fashion_order_items'
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ['id']

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
    
    @property
    def subtotal(self):
        """Calculate subtotal for this item"""
        return self.price * self.quantity
    
    def save(self, *args, **kwargs):
        # Save product details as snapshot
        if self.product and not self.product_name:
            self.product_name = self.product.name
            self.product_size = self.product.get_size_display()
            self.product_color = self.product.get_color_display()
            self.price = self.product.final_price
        
        super().save(*args, **kwargs)
        
        # Update order subtotal
        if self.order:
            self.order.subtotal = self.order.calc_total_amount
            self.order.save()
