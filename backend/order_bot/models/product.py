from django.db import models
from django.core.validators import MinValueValidator
from common.models.base import DateTimeModel, SoftDeleteModel


class Product(DateTimeModel, SoftDeleteModel):
    """
    Product model for fashion items
    """
    
    class ProductType(models.TextChoices):
        T_SHIRT = "T_SHIRT", "Áo thun"
        SHIRT = "SHIRT", "Áo sơ mi"
        DRESS = "DRESS", "Váy"
        JEANS = "JEANS", "Quần jean"
        PANTS = "PANTS", "Quần tây"
        SHORTS = "SHORTS", "Quần short"
        JACKET = "JACKET", "Áo khoác"
        SWEATER = "SWEATER", "Áo len"
        HOODIE = "HOODIE", "Áo hoodie"
        SKIRT = "SKIRT", "Chân váy"
        SHOES = "SHOES", "Giày"
        ACCESSORIES = "ACCESSORIES", "Phụ kiện"
    
    class SizeType(models.TextChoices):
        XS = "XS", "XS"
        S = "S", "S"
        M = "M", "M"
        L = "L", "L"
        XL = "XL", "XL"
        XXL = "XXL", "XXL"
        XXXL = "XXXL", "XXXL"
        FREE_SIZE = "FREE_SIZE", "Free Size"
    
    class ColorType(models.TextChoices):
        BLACK = "BLACK", "Đen"
        WHITE = "WHITE", "Trắng"
        GRAY = "GRAY", "Xám"
        RED = "RED", "Đỏ"
        BLUE = "BLUE", "Xanh dương"
        NAVY = "NAVY", "Xanh navy"
        GREEN = "GREEN", "Xanh lá"
        YELLOW = "YELLOW", "Vàng"
        PINK = "PINK", "Hồng"
        ORANGE = "ORANGE", "Cam"
        PURPLE = "PURPLE", "Tím"
        BROWN = "BROWN", "Nâu"
        BEIGE = "BEIGE", "Be"
        MULTI = "MULTI", "Nhiều màu"
    
    # Basic information
    name = models.CharField(
        max_length=200,
        verbose_name="Tên sản phẩm"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Mô tả"
    )
    
    # Category
    category = models.ForeignKey(
        'order_bot.Category',
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Danh mục"
    )
    
    # Product specifications
    product_type = models.CharField(
        max_length=20,
        choices=ProductType.choices,
        verbose_name="Loại sản phẩm"
    )
    size = models.CharField(
        max_length=20,
        choices=SizeType.choices,
        verbose_name="Kích cỡ"
    )
    color = models.CharField(
        max_length=20,
        choices=ColorType.choices,
        verbose_name="Màu sắc"
    )
    
    # Pricing
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Giá"
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        verbose_name="Giá khuyến mãi"
    )
    
    # Stock
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Số lượng tồn kho"
    )
    
    # Images
    image = models.URLField(
        blank=True,
        null=True,
        verbose_name="Hình ảnh chính"
    )
    
    # Material and care
    material = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Chất liệu"
    )
    
    # Active status
    is_active = models.BooleanField(
        default=True,
        verbose_name="Đang hoạt động"
    )
    
    # Display order
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Thứ tự hiển thị"
    )

    class Meta:
        db_table = "fashion_products"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['product_type', 'size', 'color']),
        ]

    def __str__(self):
        return f"{self.name} - {self.get_size_display()} - {self.get_color_display()}"
    
    @property
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock > 0
    
    @property
    def final_price(self):
        """Get final price (discount if available)"""
        return self.discount_price if self.discount_price else self.price
