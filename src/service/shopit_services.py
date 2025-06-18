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

async def getProductByIdService(product_id: str):
    product = await prisma.shopproducts.find_first(
        where={'id': product_id}
    )
    
    if product is None:
        raise CustomError(404, 'produk tidak ditemukan')
    
    return {
        'id': product.id,
        'name': product.name,
        'image_url': product.image_url,
        'price': product.price,
        'quantity': product.quantity
    }

async def buyProduct(user_class: str, user_group: str, buyer_email: str, payment_method: str, product_id: str, quantity: int):
    isUserExist = await prisma.accounts.find_first(
        where={ 'email': buyer_email }
    )

    if isUserExist is None:
        raise CustomError(404, 'user tidak ditemukan')
    
    if isUserExist.role == 'USER' and buyer_email != f'insys-{user_class}-{user_group}@bankit.com':
        raise CustomError(403, 'user tidak dapat mengakses data ini')

    isUserWalletExist = await prisma.userwallets.find_first(
        where={'AND': [
            {'account_id': isUserExist.id},
            {'payment_method_slug': payment_method}
        ]},
        include={'payment_method': True}
    )

    if isUserWalletExist is None:
        raise CustomError(404, 'E-Wallet user tidak ditemukan')
    
    product = await prisma.shopproducts.find_first(
        where={'id': product_id}
    )
    
    if product is None:
        raise CustomError(404, 'produk tidak ditemukan')
    
    if quantity <= 0:
        raise CustomError(422, 'jumlah pembelian minimal 1')

    if product.quantity < quantity:
        raise CustomError(400, 'inventaris produk tidak mencukupi')
    
    total_price = product.price * quantity

    if isUserWalletExist.balance < total_price:
        raise CustomError(400, 'uang E-Wallet tidak cukup')
    
    # purchase_msg = f'{isUserExist.name} membeli {quantity} buah {product.name} diShopIT via {isUserWalletExist.payment_method.payment_name}'
    purchase_msg_simple = f'Pembelian {quantity} buah {product.name} di ShopIT'

    # Kurangi Produk
    updatedProduct = await prisma.shopproducts.update(
        where={'id': product.id},
        data={'quantity': product.quantity - quantity}
    )

    if updatedProduct.quantity == 0:
        await prisma.shopproducts.update(
            where={'id': product.id},
            data={'quantity': 999}
        )
    
    # Kurangi Duit User
    updatedUserWallet = await prisma.userwallets.update(
        where={'id': isUserWalletExist.id},
        data={'balance': isUserWalletExist.balance - total_price}
    )

    # Buat Hasil Transaksi
    newPurchase = await prisma.shoptransactions.create(
        data={
            'product_id': product_id,
            'user_wallet_id': isUserWalletExist.id,
            'item_quantity': quantity,
            'total_price': total_price
        }
    )

    # Catat juga di Wallet Transaction
    newWalletTransaction = await prisma.wallettransactions.create(
        data={
            'user_wallet_id': isUserWalletExist.id,
            'balance_change': -total_price,
            'transaction_type': 'PURCHASE',
            'description': purchase_msg_simple
        }
    )

    return{
        'data': {
            'product_id': product.id,
            'purchase_id': newPurchase.id,
            'wallet_transaction_id': newWalletTransaction.id,
            'quantity': quantity,
            'total_price': total_price,
            'discount': 0,
            'current_balance': updatedUserWallet.balance
        },
        'message': purchase_msg_simple
    }