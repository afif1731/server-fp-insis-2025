import paho.mqtt.client as mqtt
import json

import src.service.shopit_services as productService

from src.utils.split_topic import topic_splitter
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