from langchain.tools import tool
from order_bot.models.product import Product
from order_bot.models.category import Category
from typing import Optional, List
from django.db.models import Q


class ProductsService:
    """Service to handle product operations for fashion shop"""
    
    @staticmethod
    @tool
    def search_products(
        product_type: Optional[str] = None,
        size: Optional[str] = None,
        color: Optional[str] = None,
        category_name: Optional[str] = None,
        max_price: Optional[float] = None,
        min_price: Optional[float] = None,
    ) -> str:
        """
        Tìm kiếm sản phẩm theo các tiêu chí.
        
        Args:
            product_type: Loại sản phẩm (T_SHIRT, SHIRT, DRESS, JEANS, PANTS, SHORTS, JACKET, SWEATER, HOODIE, SKIRT, SHOES, ACCESSORIES)
            size: Kích cỡ (XS, S, M, L, XL, XXL, XXXL, FREE_SIZE)
            color: Màu sắc (BLACK, WHITE, GRAY, RED, BLUE, NAVY, GREEN, YELLOW, PINK, ORANGE, PURPLE, BROWN, BEIGE, MULTI)
            category_name: Tên danh mục sản phẩm
            max_price: Giá tối đa
            min_price: Giá tối thiểu
        
        Returns:
            Danh sách sản phẩm phù hợp với tiêu chí tìm kiếm
        """
        
        # Start with all active products
        queryset = Product.objects.filter(is_active=True, stock__gt=0)
        
        # Apply filters
        if product_type:
            queryset = queryset.filter(product_type=product_type)
        
        if size:
            queryset = queryset.filter(size=size)
        
        if color:
            queryset = queryset.filter(color=color)
        
        if category_name:
            queryset = queryset.filter(category__name__icontains=category_name)
        
        if max_price:
            queryset = queryset.filter(
                Q(discount_price__lte=max_price) | 
                (Q(discount_price__isnull=True) & Q(price__lte=max_price))
            )
        
        if min_price:
            queryset = queryset.filter(
                Q(discount_price__gte=min_price) |
                (Q(discount_price__isnull=True) & Q(price__gte=min_price))
            )
        
        products = queryset[:10]  # Limit to 10 products
        
        if not products:
            return "Không tìm thấy sản phẩm phù hợp với yêu cầu."
        
        result = f"Tìm thấy {len(products)} sản phẩm:\n\n"
        for product in products:
            result += f"ID: {product.id}\n"
            result += f"Tên: {product.name}\n"
            result += f"Loại: {product.get_product_type_display()}\n"
            result += f"Size: {product.get_size_display()}\n"
            result += f"Màu: {product.get_color_display()}\n"
            result += f"Giá: {product.final_price:,.0f} VNĐ\n"
            result += f"Còn {product.stock} sản phẩm\n"
            if product.material:
                result += f"Chất liệu: {product.material}\n"
            result += "\n---\n\n"
        
        return result
    
    @staticmethod
    @tool
    def get_product_detail(product_id: int) -> str:
        """
        Lấy thông tin chi tiết của một sản phẩm.
        
        Args:
            product_id: ID của sản phẩm
        
        Returns:
            Thông tin chi tiết của sản phẩm
        """
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            
            result = f"Thông tin sản phẩm #{product.id}:\n\n"
            result += f"Tên: {product.name}\n"
            result += f"Danh mục: {product.category.name}\n"
            result += f"Loại: {product.get_product_type_display()}\n"
            result += f"Size: {product.get_size_display()}\n"
            result += f"Màu: {product.get_color_display()}\n"
            
            if product.discount_price:
                result += f"Giá gốc: {product.price:,.0f} VNĐ\n"
                result += f"Giá khuyến mãi: {product.discount_price:,.0f} VNĐ\n"
            else:
                result += f"Giá: {product.price:,.0f} VNĐ\n"
            
            result += f"Tồn kho: {product.stock} sản phẩm\n"
            
            if product.material:
                result += f"Chất liệu: {product.material}\n"
            
            if product.description:
                result += f"\nMô tả: {product.description}\n"
            
            return result
            
        except Product.DoesNotExist:
            return f"Không tìm thấy sản phẩm với ID {product_id}"
    
    @staticmethod
    @tool
    def check_product_availability(product_id: int, quantity: int = 1) -> str:
        """
        Kiểm tra sản phẩm có sẵn và đủ số lượng không.
        
        Args:
            product_id: ID của sản phẩm
            quantity: Số lượng cần kiểm tra
        
        Returns:
            Trạng thái sẵn có của sản phẩm
        """
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            
            if not product.is_in_stock:
                return f"Sản phẩm {product.name} hiện đang hết hàng."
            
            if product.stock < quantity:
                return f"Sản phẩm {product.name} chỉ còn {product.stock} sản phẩm, không đủ số lượng {quantity} mà bạn yêu cầu."
            
            return f"Sản phẩm {product.name} còn hàng và đủ số lượng {quantity} sản phẩm."
            
        except Product.DoesNotExist:
            return f"Không tìm thấy sản phẩm với ID {product_id}"
    
    @staticmethod
    @tool
    def get_categories() -> str:
        """
        Lấy danh sách các danh mục sản phẩm.
        
        Returns:
            Danh sách các danh mục
        """
        categories = Category.objects.filter(is_active=True).order_by('order', 'name')
        
        if not categories:
            return "Hiện chưa có danh mục sản phẩm nào."
        
        result = "Danh mục sản phẩm:\n\n"
        for category in categories:
            result += f"- {category.name}"
            if category.description:
                result += f": {category.description}"
            result += "\n"
        
        return result
    
    def create_tools(self):
        """Create list of tools for the agent"""
        return [
            self.search_products,
            self.get_product_detail,
            self.check_product_availability,
            self.get_categories,
        ]
