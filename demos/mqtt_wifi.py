import asyncio
import json
import time

import paho.mqtt.client as mqtt
from kasa import SmartPlug

plug_host = '192.168.0.104'


async def run(msg):
    plug = SmartPlug(plug_host)
    payload = json.loads(msg.payload.decode('utf-8'))
    temp = float(payload['temperature'])
    await plug.update()
    if temp < 22 and plug.is_off:
        await plug.turn_on()
    elif temp > 23 and plug.is_on:
        await plug.turn_off()


def handle_on_message(client, user_data, msg):
    asyncio.run(run(msg))


mqtt_broker = "192.168.0.170"

client = mqtt.Client("MQTT Demo Client")
client.connect(mqtt_broker)
client.loop_start()

client.subscribe("zigbee2mqtt/demo_th_sensor")

client.on_message = handle_on_message

time.sleep(1000)
