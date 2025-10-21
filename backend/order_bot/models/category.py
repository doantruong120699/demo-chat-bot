from django.db import models
from common.models.base import DateTimeModel, SoftDeleteModel


class Category(DateTimeModel, SoftDeleteModel):
    """
    Category model for fashion products
    """
    
    name = models.CharField(
        max_length=100,
        verbose_name="Tên danh mục"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Mô tả"
    )
    
    # Display order
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Thứ tự hiển thị"
    )
    
    # Active status
    is_active = models.BooleanField(
        default=True,
        verbose_name="Đang hoạt động"
    )

    class Meta:
        db_table = "fashion_categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
