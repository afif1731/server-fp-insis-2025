from src.config.prisma_config import prisma
from src.middleware.custom_error import CustomError

async def getProductCatalogService():
    products = await prisma.shopproducts.find_many(
        where={
            'quantity': {
                'gt': 0
            }
        }
    )
    
    if not products:
        raise CustomError(404, 'Tidak ada produk yang tersedia')
    
    product_list = []
    for product in products:
        product_list.append({
            'id': product.id,
            'name': product.name,
            'image_url': product.image_url,
            'price': product.price,
            'quantity': product.quantity
        })
    
    product_list.sort(key=lambda x: x['name'])
    
    return product_list