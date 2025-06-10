from src.config.prisma_config import prisma
from src.middleware.custom_error import CustomError

async def transferBalanceService(sender_email: str, receiver_email: str, payment_method: str, amount: float, mqtt_client):
    if amount <= 0:
        raise CustomError(400, 'Jumlah transfer harus lebih dari 0')

    sender = await prisma.accounts.find_first(where={'email': sender_email})
    receiver = await prisma.accounts.find_first(where={'email': receiver_email})

    if sender is None or receiver is None:
        raise CustomError(404, 'Pengirim atau penerima tidak ditemukan')

    sender_wallet = await prisma.userwallets.find_first(
        where={'AND': [
            {'account_id': sender.id},
            {'payment_method_slug': payment_method}
        ]}
    )
    receiver_wallet = await prisma.userwallets.find_first(
        where={'AND': [
            {'account_id': receiver.id},
            {'payment_method_slug': payment_method}
        ]}
    )

    if sender_wallet is None or receiver_wallet is None:
        raise CustomError(404, 'Wallet pengirim atau penerima tidak ditemukan')

    if sender_wallet.balance < amount:
        raise CustomError(400, 'Saldo pengirim tidak cukup')

    await prisma.userwallets.update(
        where={'id': sender_wallet.id},
        data={'balance': sender_wallet.balance - amount}
    )
    await prisma.userwallets.update(
        where={'id': receiver_wallet.id},
        data={'balance': receiver_wallet.balance + amount}
    )

    await prisma.wallettransactions.create(
        data={
            'user_wallet_id': sender_wallet.id,
            'transaction_type': 'TRANSFER_OUT',
            'description': f'Transfer ke {receiver_email}',
            'balance_change': -amount
        }
    )
    await prisma.wallettransactions.create(
        data={
            'user_wallet_id': receiver_wallet.id,
            'transaction_type': 'TRANSFER_IN',
            'description': f'Terima dari {sender_email}',
            'balance_change': amount
        }
    )

    topic = f"{receiver_email.replace('@','_')}/bankit/balance-update/notify"
    payload = {
        'wallet_id': receiver_wallet.id,
        'balance': receiver_wallet.balance + amount,
        'message': f'Saldo bertambah {amount} dari {sender_email}'
    }
    import json
    mqtt_client.publish(topic, json.dumps(payload))

    topic_sender = f"{sender_email.replace('@','_')}/bankit/balance-update/notify"
    payload_sender = {
        'wallet_id': sender_wallet.id,
        'balance': sender_wallet.balance - amount,
        'message': f'Saldo berkurang {amount} ke {receiver_email}'
    }
    mqtt_client.publish(topic_sender, json.dumps(payload_sender))

    return {
        'status': 'success',
        'message': f'Transfer {amount} ke {receiver_email} berhasil'
    }