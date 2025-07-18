import paho.mqtt.client as mqtt
import asyncio

import src.controller.get_account_controller as getAccountController
import src.controller.shopit_controller as productController
from src.config.mqtt_config import connect_mqtt, MQTT_URL
from src.config.prisma_config import prisma
from src.controller.transfer_controller import handle_transfer_balance, handle_ask_balance

LOOP = None  # Global event loop
stop_event = asyncio.Event()

def async_callback_wrapper(coro_func):
    def wrapper(client, userdata, message):
        future = asyncio.run_coroutine_threadsafe(
            coro_func(client, userdata, message),
            LOOP
        )
        def handle_exception(f):
            try:
                f.result()
            except Exception as e:
                print(f"Async callback error: {e}")
        future.add_done_callback(handle_exception)
    return wrapper

TOPIC_HANDLERS = {
    'bankit/account-identity/request': async_callback_wrapper(getAccountController.getAccountController),
    'bankit/wallet-identity/request': async_callback_wrapper(getAccountController.getWalletController),
    'bankit/wallet-history/request': async_callback_wrapper(getAccountController.getWalletHistoryController),
    'bankit/+/transfer/send/request': async_callback_wrapper(handle_transfer_balance),
    'bankit/+/give-balance/request': async_callback_wrapper(handle_ask_balance),

    'shopit/product-catalog/request': async_callback_wrapper(productController.getProductCatalogController),
    'shopit/product-detail/request': async_callback_wrapper(productController.getProductByIdController),
    'shopit/buy/request': async_callback_wrapper(productController.buyProductController),
}

def onConnectHandler(client: mqtt.Client, userdata, flags, rc):
    client.subscribe('+/+/bankit/account-identity/request')
    client.subscribe('+/+/bankit/wallet-identity/request')
    client.subscribe('+/+/bankit/wallet-history/request')
    client.subscribe('+/+/bankit/+/transfer/send/request')
    client.subscribe('+/+/bankit/+/give-balance/request')
    
    client.subscribe('+/+/shopit/product-catalog/request')
    client.subscribe('+/+/shopit/product-detail/request')
    client.subscribe('+/+/shopit/buy/request')

def onMessageHandler(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    topic_parts = message.topic.split('/')
    if len(topic_parts) > 4 and (topic_parts[4] == 'transfer' or topic_parts[4] == 'give-balance' or topic_parts[4] == 'live-history'):
        topic_parts[3] = '+'
    
    key = '/'.join(topic_parts[2:])
    handler = TOPIC_HANDLERS.get(key)
    if handler:
        handler(client, userdata, message)

async def main():
    global LOOP
    LOOP = asyncio.get_running_loop()  # Ini penting dan aman di Python 3.9

    await prisma.connect()
    client = connect_mqtt(onMessage=onMessageHandler, onConnect=onConnectHandler)

    print(f'📡 Listening to [{MQTT_URL}]')
    print('🚪 Tekan tombol [Ctrl + C] untuk keluar')

    try:
        await asyncio.to_thread(client.loop_forever)
    except KeyboardInterrupt:
        print("\n🛑 Ctrl+C ditekan.")
    finally:
        print("🔌 Cleaning Process...")
        client.disconnect()
        await prisma.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("✅ Disconnected. Exiting.")
