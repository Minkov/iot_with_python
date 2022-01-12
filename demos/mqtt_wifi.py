import asyncio
import json
import time

import paho.mqtt.client as mqtt
from kasa import SmartPlug


async def r(msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    current_temperature = float(payload['temperature'])
    heating_plug = SmartPlug('192.168.0.104')
    await heating_plug.update()
    if current_temperature < 19 and heating_plug.is_off:
        await heating_plug.turn_on()
    elif current_temperature > 21 and heating_plug.is_on:
        await heating_plug.turn_off()


def handle_on_message(client, user_data, msg):
    asyncio.run(r(msg))


mqtt_broker = "192.168.0.170"

client = mqtt.Client("MQTT demo Client")
client.connect(mqtt_broker)
client.loop_start()

client.subscribe("zigbee2mqtt/demo_th_sensor")

client.on_message = handle_on_message

time.sleep(1000)
