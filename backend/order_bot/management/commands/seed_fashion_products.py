from django.core.management.base import BaseCommand
from order_bot.models.category import Category
from order_bot.models.product import Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seed fashion products and categories'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding fashion data...')
        
        # Clear existing data
        Product.objects.all().delete()
        Category.objects.all().delete()
        
        # Create categories
        categories_data = [
            {'name': 'Áo', 'description': 'Áo thun, áo sơ mi, áo khoác...', 'order': 1},
            {'name': 'Quần', 'description': 'Quần jean, quần tây, quần short...', 'order': 2},
            {'name': 'Váy', 'description': 'Váy đầm, chân váy...', 'order': 3},
            {'name': 'Giày dép', 'description': 'Giày thể thao, giày cao gót, dép...', 'order': 4},
            {'name': 'Phụ kiện', 'description': 'Túi xách, nón, khăn...', 'order': 5},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data, is_active=True)
            categories[cat_data['name']] = category
            self.stdout.write(f'  Created category: {category.name}')
        
        # Create products
        products_data = [
            # Áo thun
            {
                'name': 'Áo thun basic trắng',
                'description': 'Áo thun cotton 100%, form regular, phù hợp mặc hàng ngày',
                'category': categories['Áo'],
                'product_type': Product.ProductType.T_SHIRT,
                'size': Product.SizeType.M,
                'color': Product.ColorType.WHITE,
                'price': Decimal('150000'),
                'discount_price': Decimal('120000'),
                'stock': 50,
                'is_active': True,
            },
            {
                'name': 'Áo thun basic đen',
                'description': 'Áo thun cotton 100%, form regular, dễ phối đồ',
                'category': categories['Áo'],
                'product_type': Product.ProductType.T_SHIRT,
                'size': Product.SizeType.L,
                'color': Product.ColorType.BLACK,
                'price': Decimal('150000'),
                'stock': 40,
                'is_active': True,
            },
            {
                'name': 'Áo thun oversize xám',
                'description': 'Áo thun form oversize trendy, chất liệu mát mẻ',
                'category': categories['Áo'],
                'product_type': Product.ProductType.T_SHIRT,
                'size': Product.SizeType.XL,
                'color': Product.ColorType.GRAY,
                'price': Decimal('180000'),
                'discount_price': Decimal('150000'),
                'stock': 30,
                'is_active': True,
            },
            
            # Áo sơ mi
            {
                'name': 'Áo sơ mi trắng công sở',
                'description': 'Áo sơ mi vải kate cao cấp, form slim fit, phù hợp đi làm',
                'category': categories['Áo'],
                'product_type': Product.ProductType.SHIRT,
                'size': Product.SizeType.M,
                'color': Product.ColorType.WHITE,
                'price': Decimal('250000'),
                'stock': 25,
                'is_active': True,
            },
            {
                'name': 'Áo sơ mi xanh navy',
                'description': 'Áo sơ mi vải oxford, phong cách lịch lãm',
                'category': categories['Áo'],
                'product_type': Product.ProductType.SHIRT,
                'size': Product.SizeType.L,
                'color': Product.ColorType.NAVY,
                'price': Decimal('280000'),
                'discount_price': Decimal('220000'),
                'stock': 20,
                'is_active': True,
            },
            
            # Áo khoác
            {
                'name': 'Áo khoác denim xanh',
                'description': 'Áo khoác jean wash nhẹ, form regular, phong cách street',
                'category': categories['Áo'],
                'product_type': Product.ProductType.JACKET,
                'size': Product.SizeType.L,
                'color': Product.ColorType.BLUE,
                'price': Decimal('450000'),
                'discount_price': Decimal('380000'),
                'stock': 15,
                'is_active': True,
            },
            {
                'name': 'Áo hoodie đen basic',
                'description': 'Áo hoodie nỉ mềm mại, ấm áp, có túi kangaroo',
                'category': categories['Áo'],
                'product_type': Product.ProductType.HOODIE,
                'size': Product.SizeType.XL,
                'color': Product.ColorType.BLACK,
                'price': Decimal('350000'),
                'stock': 35,
                'is_active': True,
            },
            
            # Quần jean
            {
                'name': 'Quần jean skinny đen',
                'description': 'Quần jean co giãn, form skinny, ôm dáng',
                'category': categories['Quần'],
                'product_type': Product.ProductType.JEANS,
                'size': Product.SizeType.M,
                'color': Product.ColorType.BLACK,
                'price': Decimal('350000'),
                'discount_price': Decimal('280000'),
                'stock': 40,
                'is_active': True,
            },
            {
                'name': 'Quần jean baggy xanh nhạt',
                'description': 'Quần jean form baggy trendy, phong cách unisex',
                'category': categories['Quần'],
                'product_type': Product.ProductType.JEANS,
                'size': Product.SizeType.L,
                'color': Product.ColorType.BLUE,
                'price': Decimal('380000'),
                'discount_price': Decimal('320000'),
                'stock': 30,
                'is_active': True,
            },
            
            # Quần tây
            {
                'name': 'Quần tây công sở đen',
                'description': 'Quần tây vải tuyết mưa, form slim, phù hợp đi làm',
                'category': categories['Quần'],
                'product_type': Product.ProductType.PANTS,
                'size': Product.SizeType.M,
                'color': Product.ColorType.BLACK,
                'price': Decimal('300000'),
                'stock': 25,
                'is_active': True,
            },
            {
                'name': 'Quần tây xám nhạt',
                'description': 'Quần tây vải cao cấp, form regular, dễ phối',
                'category': categories['Quần'],
                'product_type': Product.ProductType.PANTS,
                'size': Product.SizeType.L,
                'color': Product.ColorType.GRAY,
                'price': Decimal('320000'),
                'discount_price': Decimal('260000'),
                'stock': 20,
                'is_active': True,
            },
            
            # Quần short
            {
                'name': 'Quần short kaki be',
                'description': 'Quần short kaki mùa hè, thoáng mát',
                'category': categories['Quần'],
                'product_type': Product.ProductType.SHORTS,
                'size': Product.SizeType.M,
                'color': Product.ColorType.BEIGE,
                'price': Decimal('200000'),
                'stock': 30,
                'is_active': True,
            },
            
            # Váy
            {
                'name': 'Váy đầm hoa nhí',
                'description': 'Váy đầm họa tiết hoa nhỏ xinh, phong cách vintage',
                'category': categories['Váy'],
                'product_type': Product.ProductType.DRESS,
                'size': Product.SizeType.M,
                'color': Product.ColorType.MULTI,
                'price': Decimal('380000'),
                'discount_price': Decimal('320000'),
                'stock': 20,
                'is_active': True,
            },
            {
                'name': 'Chân váy xếp ly đen',
                'description': 'Chân váy xếp ly dài, thanh lịch, phù hợp đi làm',
                'category': categories['Váy'],
                'product_type': Product.ProductType.SKIRT,
                'size': Product.SizeType.S,
                'color': Product.ColorType.BLACK,
                'price': Decimal('250000'),
                'stock': 25,
                'is_active': True,
            },
            
            # Giày
            {
                'name': 'Giày thể thao trắng',
                'description': 'Giày sneaker trắng basic, dễ phối đồ, đế êm',
                'category': categories['Giày dép'],
                'product_type': Product.ProductType.SHOES,
                'size': Product.SizeType.FREE_SIZE,
                'color': Product.ColorType.WHITE,
                'price': Decimal('450000'),
                'discount_price': Decimal('380000'),
                'stock': 30,
                'is_active': True,
            },
            {
                'name': 'Giày thể thao đen',
                'description': 'Giày sneaker đen, phong cách sporty',
                'category': categories['Giày dép'],
                'product_type': Product.ProductType.SHOES,
                'size': Product.SizeType.FREE_SIZE,
                'color': Product.ColorType.BLACK,
                'price': Decimal('480000'),
                'stock': 25,
                'is_active': True,
            },
        ]
        
        for product_data in products_data:
            product = Product.objects.create(**product_data)
            self.stdout.write(f'  Created product: {product.name} - {product.final_price} VNĐ (stock: {product.stock})')
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully seeded {len(products_data)} products!'))
