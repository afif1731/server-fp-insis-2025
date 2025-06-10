import paho.mqtt.client as mqtt
import json

import src.service.get_account_service as getAccountService

from src.middleware.validator import do_validate
from src.utils.split_topic import topic_splitter
from src.utils.validator_helper import validate_email
from src.validator.get_account_validator import getAccountValidator, getWalletValidator, getWalletHistoryValidator
from src.middleware.custom_response import CustomResponse
from src.middleware.custom_error import CustomError

async def getAccountController(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    try:
        topic_parts = topic_splitter(message.topic)
        callback_topic = f'{topic_parts[0]}/{topic_parts[1]}/bankit/account-identity/response'
        data = do_validate(getAccountValidator, json.loads(message.payload))
        email = validate_email(data['email']) # Somehow validator email dari lib donttrust nge-return email kita false, jadi bikin validator sendiri buat email

        result = await getAccountService.getAccountPublishService(user_class=topic_parts[0], user_group=topic_parts[1], user_email=email)
        response = CustomResponse(200, 'sukses mendapatkan data user', result)

        client.publish(topic=callback_topic, payload=json.dumps(response.JSON()))
    except CustomError as err:
        print(err.JSON())
        client.publish(topic=callback_topic, payload=json.dumps(err.JSON()))

async def getWalletController(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    try:
        topic_parts = topic_splitter(message.topic)
        callback_topic = f'{topic_parts[0]}/{topic_parts[1]}/bankit/wallet-identity/response'

        data = do_validate(getWalletValidator, json.loads(message.payload))
        email = validate_email(data['email']) # Somehow validator email dari lib donttrust nge-return email kita false, jadi bikin validator sendiri buat email
        
        result = await getAccountService.getWalletPublishService(user_class=topic_parts[0], user_group=topic_parts[1], user_email=email, payment_method=data['payment_method'])
        response = CustomResponse(200, 'sukses mendapatkan data wallet user', result)

        client.publish(topic=callback_topic, payload=json.dumps(response.JSON()))
    except CustomError as err:
        print(err.JSON())
        client.publish(topic=callback_topic, payload=json.dumps(err.JSON()))

async def getWalletHistoryController(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    try:
        topic_parts = topic_splitter(message.topic)
        callback_topic = f'{topic_parts[0]}/{topic_parts[1]}/bankit/wallet-history/response'

        data = do_validate(getWalletHistoryValidator, json.loads(message.payload))
        email = validate_email(data['email']) # Somehow validator email dari lib donttrust nge-return email kita false, jadi bikin validator sendiri buat email
        
        result = await getAccountService.getWalletHistoryService(user_class=topic_parts[0], user_group=topic_parts[1], user_email=email, payment_method=data['payment_method'])
        response = CustomResponse(200, 'sukses mendapatkan history transaksi wallet', result)

        client.publish(topic=callback_topic, payload=json.dumps(response.JSON()))
    except CustomError as err:
        print(err.JSON())
        client.publish(topic=callback_topic, payload=json.dumps(err.JSON()))