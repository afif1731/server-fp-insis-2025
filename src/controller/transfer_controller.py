from src.service.transfer_service import transferBalanceService
from src.validator.transfer_validator import validate_transfer_payload
from src.middleware.custom_error import CustomError

import json

async def handle_transfer_balance(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode())
        is_valid, error_msg = validate_transfer_payload(payload)
        if not is_valid:
            raise CustomError(400, error_msg)
        result = await transferBalanceService(
            sender_email=payload['sender_email'],
            receiver_email=payload['receiver_email'],
            payment_method=payload['payment_method'],
            amount=payload['amount'],
            mqtt_client=client
        )

        response_topic = payload.get('response_topic')
        if response_topic:
            client.publish(response_topic, json.dumps(result))
    except Exception as e:
        error_payload = {'status': 'error', 'message': str(e)}
        response_topic = payload.get('response_topic', 'bankit/balance-transfer/response')
        client.publish(response_topic, json.dumps(error_payload))