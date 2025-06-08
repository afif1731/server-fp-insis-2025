from src.config.prisma_config import prisma
from src.middleware.custom_error import CustomError

async def getAccountPublishService(user_class: str, user_group: str, user_email: str):
    isUserExist = await prisma.accounts.find_first(
        where={ 'email': user_email }
    )

    if isUserExist is None:
        raise CustomError(404, 'user tidak ditemukan')
    
    if (isUserExist.role != 'USER') or (user_email != f'insys-{user_class}-{user_group}@bankit.com'):
        print('email tidak sesuai')
        raise CustomError(403, 'user tidak dapat mengakses data ini')

    return{
        'id': isUserExist.id,
        'name': isUserExist.name,
        'email': isUserExist.email
    }

async def getWalletPublishService(user_class: str, user_group: str, user_email: str, payment_method: str):
    isUserExist = await prisma.accounts.find_first(
        where={ 'email': user_email }
    )

    if isUserExist is None:
        raise CustomError(404, 'user tidak ditemukan')
    
    if isUserExist.role == 'USER' and user_email != f'insys-{user_class}-{user_group}@bankit.com':
        raise CustomError(403, 'user tidak dapat mengakses data ini')

    isPaymentMethodExist = await prisma.paymentmethods.find_first(
        where={ 'payment_slug': payment_method }
    )

    if isPaymentMethodExist is None:
        raise CustomError(404, 'metode pembayaran tidak ditemukan')
    
    userWallet = await prisma.userwallets.find_first(
        where={'AND': [
            {'account_id': isUserExist.id},
            {'payment_method_slug': payment_method}
        ]}
    )
    
    return {
        'id': userWallet.id,
        'wallet_name': userWallet.wallet_name,
        'payment_method': payment_method,
        'balance': userWallet.balance
    }