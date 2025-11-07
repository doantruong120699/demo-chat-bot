import { useState } from 'react';

const ProductCard = ({ product, onCardClick }) => {
  const [imageError, setImageError] = useState(false);
  
  const formatPrice = (price) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(price);
  };

  const hasDiscount = product.discount_price && product.discount_price < product.price;

  return (
    <div 
      className="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer hover:shadow-xl transition-shadow duration-300"
      onClick={() => onCardClick(product)}
    >
      {/* Product Image */}
      <div className="relative h-48 bg-gray-200 overflow-hidden">
        {product.image && !imageError ? (
          <img 
            src={product.image} 
            alt={product.name}
            className="w-full h-full object-cover"
            onError={() => setImageError(true)}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-purple-100 to-pink-100">
            <svg className="w-20 h-20 text-purple-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        )}
        
        {/* Stock Badge */}
        {product.stock <= 5 && product.stock > 0 && (
          <div className="absolute top-2 right-2 bg-yellow-500 text-white text-xs font-bold px-2 py-1 rounded">
            Còn {product.stock}
          </div>
        )}
        
        {/* Discount Badge */}
        {hasDiscount && (
          <div className="absolute top-2 left-2 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">
            SALE
          </div>
        )}
      </div>

      {/* Product Info */}
      <div className="p-4">
        <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 min-h-[2.5rem]">
          {product.name}
        </h3>
        
        <div className="flex items-center gap-2 mb-2 text-sm text-gray-600">
          <span className="bg-gray-100 px-2 py-1 rounded">{product.size}</span>
          <span className="bg-gray-100 px-2 py-1 rounded">{product.color}</span>
        </div>

        {/* Price */}
        <div className="mt-2">
          {hasDiscount ? (
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold text-red-600">
                {formatPrice(product.discount_price)}
              </span>
              <span className="text-sm text-gray-500 line-through">
                {formatPrice(product.price)}
              </span>
            </div>
          ) : (
            <span className="text-lg font-bold text-purple-600">
              {formatPrice(product.final_price)}
            </span>
          )}
        </div>

        {/* Material */}
        {product.material && (
          <p className="text-xs text-gray-500 mt-2">
            {product.material}
          </p>
        )}
      </div>
    </div>
  );
};

export default ProductCard;
