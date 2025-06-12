from src.config.prisma_config import prisma
from src.middleware.custom_error import CustomError

async def transferBalanceService(sender_email: str, receiver_email: str, sender_payment_method: str, receiver_payment_method: str, amount: int, user_class: str, user_group: str):
    if type(amount) != int:
        raise CustomError(422, 'Jumlah transfer harus berupa bilangan bulat positif')
    
    if amount <= 0:
        raise CustomError(422, 'Jumlah transfer harus lebih dari 0')

    sender = await prisma.accounts.find_first(where={'email': sender_email})
    receiver = await prisma.accounts.find_first(where={'email': receiver_email})

    if sender is None:
        raise CustomError(404, 'Pengirim tidak ditemukan')

    if receiver is None:
        raise CustomError(404, 'Penerima tidak ditemukan')

    if (receiver.role != 'USER') or (sender_email != f'insys-{user_class}-{user_group}@bankit.com'):
        raise CustomError(403, 'user tidak dapat mengakses data ini')

    sender_wallet = await prisma.userwallets.find_first(
        where={'AND': [
            {'account_id': sender.id},
            {'payment_method_slug': sender_payment_method}
        ]},
        include={'payment_method': True}
    )

    receiver_wallet = await prisma.userwallets.find_first(
        where={'AND': [
            {'account_id': receiver.id},
            {'payment_method_slug': receiver_payment_method},
        ]},
        include={'payment_method': True}
    )

    if sender_wallet is None:
        raise CustomError(404, 'E-Wallet pengirim tidak ditemukan')
    
    if receiver_wallet is None:
        raise CustomError(404, 'E-Wallet penerima tidak ditemukan')

    if sender_wallet.balance < amount:
        raise CustomError(400, 'Saldo pengirim tidak cukup')

    updated_sender_wallet = await prisma.userwallets.update(
        where={'id': sender_wallet.id},
        data={'balance': sender_wallet.balance - amount}
    )

    updated_receiver_wallet = await prisma.userwallets.update(
        where={'id': receiver_wallet.id},
        data={'balance': receiver_wallet.balance + amount}
    )

    sender_transaction = await prisma.wallettransactions.create(
        data={
            'user_wallet_id': sender_wallet.id,
            'transaction_type': 'TRANSFER',
            'description': f'Transfer ke {receiver_email}',
            'balance_change': -amount
        }
    )

    receiver_transaction = await prisma.wallettransactions.create(
        data={
            'user_wallet_id': receiver_wallet.id,
            'transaction_type': 'TRANSFER',
            'description': f'Terima transfer dari {sender_email}',
            'balance_change': amount
        }
    )

    return {
        'sender_result': {
            'transfer_id': sender_transaction.id,
            'sender_email': sender.email,
            'current_balance': updated_sender_wallet.balance
        },
        'receiver_result': {
            'transfer_id': receiver_transaction.id,
            'receiver_email': receiver.email,
            'current_balance': updated_receiver_wallet.balance
        },
        'receiver_name': receiver.name,
        'receiver_payment_method': receiver_wallet.payment_method.payment_name,
        'sender_name': sender.name,
        'sender_payment_method': sender_wallet.payment_method.payment_name
    }

async def askBalanceService(user_class: str, user_group: str, user_email: str, payment_method: str):
    isUserExist = await prisma.accounts.find_first(
        where={ 'email': user_email }
    )

    if isUserExist is None:
        raise CustomError(404, 'user tidak ditemukan')
    
    if (isUserExist.role != 'USER') or (user_email != f'insys-{user_class}-{user_group}@bankit.com'):
        print('email tidak sesuai')
        raise CustomError(403, 'user tidak dapat mengakses data ini')
    
    userWallet = await prisma.userwallets.find_first(
        where={'AND': [
            {'account_id': isUserExist.id},
            {'payment_method_slug': payment_method},
        ]},
        include={'payment_method': True}
    )

    if userWallet is None:
        raise CustomError(404, 'E-Wallet user tidak ditemukan')
    
    updatedWallet = await prisma.userwallets.update(
        where={'id': userWallet.id},
        data={
            'balance': userWallet.balance + 10000
        }
    )

    return {
        'username': isUserExist.name,
        'payment_method': payment_method,
        'user_wallet_id': userWallet.id,
        'current_balance': updatedWallet.balance
    }