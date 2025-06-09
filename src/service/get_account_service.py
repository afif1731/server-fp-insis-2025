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

async def getWalletHistoryService(user_class: str, user_group: str, user_email: str, payment_method: str):
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

    if userWallet is None:
        raise CustomError(404, 'wallet tidak ditemukan')
    
    # Get wallet transaction history, ordered by most recent first
    transactions = await prisma.wallettransactions.find_many(
        where={'user_wallet_id': userWallet.id},
        order={'created_at': 'desc'},
        include={'user_wallet': True}
    )
    
    # Format transaction history
    history = []
    for transaction in transactions:
        history.append({
            'id': transaction.id,
            'transaction_type': transaction.transaction_type,
            'description': transaction.description,
            'balance_change': transaction.balance_change,
            'created_at': transaction.created_at.isoformat(),
            'amount': abs(transaction.balance_change),
            'type': 'credit' if transaction.balance_change > 0 else 'debit'
        })
    
    return {
        'wallet_id': userWallet.id,
        'wallet_name': userWallet.wallet_name,
        'payment_method': payment_method,
        'current_balance': userWallet.balance,
        'transaction_count': len(history),
        'transactions': history
    }