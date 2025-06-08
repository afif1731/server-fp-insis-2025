import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import sys
import os

load_dotenv()

MQTT_BROKER = os.getenv('MQTT_BROKER', 'localhost')
MQTT_PORT = os.getenv('MQTT_PORT', '1883')
MQTT_ADMIN = os.getenv('MQTT_ADMIN', 'Admien')
MQTT_PASS = os.getenv('MQTT_PASS', 'Admin##1')
MQTT_URL = os.getenv('MQTT_URL', 'mqtt://localhost:1883')

client = mqtt.Client()

def on_connect_fail(client, userdata):
    print("❌ MQTT connection failed!")
    sys.exit(1)

def connect_mqtt(onMessage, onConnect):
    client.username_pw_set(username=MQTT_ADMIN, password=MQTT_PASS)
    client.on_message = onMessage
    client.on_connect = onConnect
    client.on_connect_fail = on_connect_fail
    client.connect(MQTT_BROKER, int(MQTT_PORT), 60)
    return client