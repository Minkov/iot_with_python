import json
import time

import paho.mqtt.client as mqtt

mqtt_broker = "192.168.0.170"


def handle_on_message(client, user_data, msg):
    payload_str = msg.payload.decode('utf-8')
    try:
        payload = json.loads(payload_str)
    except:
        payload = payload_str

    print(f'{msg.topic}: {payload}')


client = mqtt.Client("MQTT Demo Client")
client.connect(mqtt_broker)
client.loop_start()

client.subscribe("#")

client.on_message = handle_on_message

payload = json.dumps({
    "mode": "color",
    "red": 255,
    "green": 0,
    "blue": 0,
    "gain": 100,
    "white": 255,
    "effect": 0,
    "turn": "on",
    "transition": 500
})

client.publish('shellies/shellyrgbw2-DE0150/color/0/set', payload)

time.sleep(1000)
