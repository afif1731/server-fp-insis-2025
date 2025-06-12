from prisma import enums
import paho.mqtt.client as mqtt
import json

from src.middleware.custom_response import CustomResponse

def send_live_update_balance(client: mqtt.Client, user_class: str, user_group: str, payment_method: str, transaction_type: enums.TransactionType, amount: int, updated_balance: int, message: str):
    send_topic = f'{user_class}/{user_group}/bankit/{payment_method}/live-history'

    result = {
        'amount': amount,
        'transaction_type': transaction_type,
        'current_balance': updated_balance
    }

    response = CustomResponse(200, message, result)
    client.publish(topic=send_topic, payload=json.dumps(response.JSON()))