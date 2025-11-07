import { useState } from 'react';

const ProductModal = ({ product, isOpen, onClose }) => {
  const [imageError, setImageError] = useState(false);
  
  if (!isOpen || !product) return null;

  const formatPrice = (price) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(price);
  };

  const hasDiscount = product.discount_price && product.discount_price < product.price;

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 z-[60] flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div 
        className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <div className="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-center">
          <h2 className="text-xl font-bold text-gray-900">Product Details</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 p-2 rounded-full hover:bg-gray-100 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Image */}
          <div className="relative w-full h-96 bg-gray-200 rounded-lg overflow-hidden mb-6">
            {product.image && !imageError ? (
              <img 
                src={product.image} 
                alt={product.name}
                className="w-full h-full object-contain"
                onError={() => setImageError(true)}
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-purple-100 to-pink-100">
                <svg className="w-32 h-32 text-purple-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            )}
            
            {/* Badges */}
            {hasDiscount && (
              <div className="absolute top-4 left-4 bg-red-500 text-white text-sm font-bold px-3 py-1 rounded">
                SALE
              </div>
            )}
            {product.stock <= 5 && product.stock > 0 && (
              <div className="absolute top-4 right-4 bg-yellow-500 text-white text-sm font-bold px-3 py-1 rounded">
                Only {product.stock} left
              </div>
            )}
          </div>

          {/* Product Info */}
          <div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">
              {product.name}
            </h3>
            
            {/* ID */}
            <p className="text-sm text-gray-500 mb-4">
              Product ID: #{product.id}
            </p>

            {/* Price */}
            <div className="mb-6">
              {hasDiscount ? (
                <div>
                  <div className="flex items-center gap-3">
                    <span className="text-3xl font-bold text-red-600">
                      {formatPrice(product.discount_price)}
                    </span>
                    <span className="text-xl text-gray-500 line-through">
                      {formatPrice(product.price)}
                    </span>
                  </div>
                  <p className="text-sm text-red-600 mt-1">
                    Save {formatPrice(product.price - product.discount_price)}
                  </p>
                </div>
              ) : (
                <span className="text-3xl font-bold text-purple-600">
                  {formatPrice(product.final_price)}
                </span>
              )}
            </div>

            {/* Specifications */}
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Type</p>
                <p className="font-semibold text-gray-900">{product.product_type}</p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Size</p>
                <p className="font-semibold text-gray-900">{product.size}</p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Color</p>
                <p className="font-semibold text-gray-900">{product.color}</p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Stock</p>
                <p className="font-semibold text-gray-900">
                  {product.stock > 0 ? `${product.stock} available` : 'Out of stock'}
                </p>
              </div>
            </div>

            {/* Material */}
            {product.material && (
              <div className="mb-6">
                <h4 className="font-semibold text-gray-900 mb-2">Material</h4>
                <p className="text-gray-600">{product.material}</p>
              </div>
            )}

            {/* Category */}
            {product.category && (
              <div className="mb-6">
                <h4 className="font-semibold text-gray-900 mb-2">Category</h4>
                <p className="text-gray-600">{product.category}</p>
              </div>
            )}

            {/* Description */}
            {product.description && (
              <div className="mb-6">
                <h4 className="font-semibold text-gray-900 mb-2">Description</h4>
                <p className="text-gray-600 whitespace-pre-wrap">{product.description}</p>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-3 pt-4 border-t">
              <button
                onClick={onClose}
                className="flex-1 bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
              >
                Select This Product
              </button>
              <button
                onClick={onClose}
                className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-3 px-6 rounded-lg transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductModal;
