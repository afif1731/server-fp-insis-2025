import paho.mqtt.client as mqtt
import json

from src.middleware.validator import do_validate
from src.utils.split_topic import topic_splitter
from src.utils.validator_helper import validate_email
from src.service.transfer_service import transferBalanceService
from src.validator.transfer_validator import transferBalanceValidator
from src.middleware.custom_response import CustomResponse

import json

async def handle_transfer_balance(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    try:
        topic_parts = topic_splitter(message.topic)
        sender_payment_method = topic_parts[3]

        sender_callback_topic = f'{topic_parts[0]}/{topic_parts[1]}/bankit/{sender_payment_method}/transfer/send/response'

        data = do_validate(transferBalanceValidator, json.loads(message.payload))
        sender_email = validate_email(data['sender_email'])
        receiver_email = validate_email(data['receiver_email'])
        
        result = await transferBalanceService(
            sender_email=sender_email,
            receiver_email=receiver_email,
            sender_payment_method=sender_payment_method,
            receiver_payment_method=data['receiver_payment_method'],
            amount=data['amount'],
            user_class=topic_parts[0],
            user_group=topic_parts[1]
        )
        sender_response = CustomResponse(200, f'sukses mengirim transfer ke E-Wallet {result['receiver_payment_method']} milik user {receiver_email}', result['sender_result'])
        receiver_response = CustomResponse(200, f'sukses mendapat transfer dari E-Wallet {result['sender_payment_method']} milik user {sender_email}', result['receiver_result'])

        receiver_class, receiver_group = extract_email_values(receiver_email)
        receiver_callback_topic = f'{receiver_class}/{receiver_group}/bankit/{data['receiver_payment_method']}/transfer/receive'
        
        client.publish(topic=sender_callback_topic, payload=json.dumps(sender_response.JSON())) # Publish ke sender
        client.publish(topic=receiver_callback_topic, payload=json.dumps(receiver_response.JSON())) # Publish ke Receiver
    except Exception as err:
        print(err.JSON())
        client.publish(topic=sender_callback_topic, payload=json.dumps(err.JSON()))

def extract_email_values(s: str):
    try:
        # Ambil bagian sebelum '@'
        local_part = s.split('@')[0]
        # Pisahkan berdasarkan tanda '-'
        parts = local_part.split('-')
        if len(parts) >= 3:
            return parts[1], parts[2]  # Kelas dan Kelompok
        else:
            raise ValueError("Format string tidak sesuai")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None, None