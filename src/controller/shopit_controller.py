import paho.mqtt.client as mqtt
import json

from src.service.live_balance_history import send_live_update_balance
import src.service.shopit_services as productService

from src.middleware.validator import do_validate
from src.utils.split_topic import topic_splitter
from src.utils.validator_helper import validate_email
from src.validator.shopit_validator import getProductByIdValidator, buyProductValidator
from src.middleware.custom_response import CustomResponse
from src.middleware.custom_error import CustomError

async def getProductCatalogController(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    try:
        topic_parts = topic_splitter(message.topic)
        callback_topic = f'{topic_parts[0]}/{topic_parts[1]}/shopit/product-catalog/response'
        
        result = await productService.getProductCatalogService()
        response = CustomResponse(200, 'sukses mendapatkan katalog produk', result)

        client.publish(topic=callback_topic, payload=json.dumps(response.JSON()))
    except CustomError as err:
        print(err.JSON())
        client.publish(topic=callback_topic, payload=json.dumps(err.JSON()))

async def getProductByIdController(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    try:
        topic_parts = topic_splitter(message.topic)
        callback_topic = f'{topic_parts[0]}/{topic_parts[1]}/shopit/product-detail/response'
        
        data = do_validate(getProductByIdValidator, json.loads(message.payload))
        
        result = await productService.getProductByIdService(data['product_id'])
        response = CustomResponse(200, 'sukses mendapatkan detail produk', result)

        client.publish(topic=callback_topic, payload=json.dumps(response.JSON()))
    except CustomError as err:
        print(err.JSON())
        client.publish(topic=callback_topic, payload=json.dumps(err.JSON()))

async def buyProductController(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    try:
        topic_parts = topic_splitter(message.topic)
        callback_topic = f'{topic_parts[0]}/{topic_parts[1]}/shopit/buy/response'

        data = do_validate(buyProductValidator, json.loads(message.payload))
        email = validate_email(data['buyer_email'])

        result = await productService.buyProduct(
            user_class=topic_parts[0],
            user_group=topic_parts[1],
            buyer_email=email,
            payment_method=data['payment_method'],
            product_id=data['product_id'],
            quantity=data['quantity']
        )
        response = CustomResponse(200, 'transaksi ShopIT berhasil', result['data'])
        
        client.publish(topic=callback_topic, payload=json.dumps(response.JSON()))
        send_live_update_balance(
            client=client,
            user_class=topic_parts[0],
            user_group=topic_parts[1],
            payment_method=data['payment_method'],
            transaction_type='PURCHASE',
            amount=-result['data']['total_price'],
            updated_balance=result['data']['current_balance'],
            message=result['message']
            )
    except CustomError as err:
        print(err.JSON())
        client.publish(topic=callback_topic, payload=json.dumps(err.JSON()))