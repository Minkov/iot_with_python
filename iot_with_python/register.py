import json
from json import JSONDecodeError

import paho.mqtt.client as mqtt

from iot_with_python.demo_app.models import ActionCondition, ActionDevice, ConsumerDevice


def should_run_with_string(operation, condition_value, device_value):
    return condition_value == device_value \
        if operation == ActionCondition.EQ_OPERATION \
        else condition_value != device_value


def should_run_with_number(operation, condition_value, device_value):
    if operation == ActionCondition.LT_OPERATION:
        return device_value < condition_value
    elif operation == ActionCondition.GT_OPERATION:
        return condition_value < device_value


def should_run_with_bool(operation, condition_value, device_value):
    if operation == ActionCondition.EQ_OPERATION:
        return device_value.lower() == condition_value.lower()
    elif operation == ActionCondition.NE_OPERATION:
        return device_value.lower() != condition_value.lower()


def get_condition_payload(condition, device_payload):
    device_value_string = str(device_payload[condition.payload_key])
    condition_value_string = condition.value
    if condition.value_type == ActionCondition.VALUE_TYPE_STRING:
        should_run = should_run_with_string(condition.operation, condition_value_string, device_value_string)
    elif condition.value_type == ActionCondition.VALUE_TYPE_NUMBER:
        should_run = should_run_with_number(condition.operation, int(condition_value_string), int(device_value_string))
    else:
        should_run = should_run_with_bool(condition.operation, condition_value_string, device_value_string)

    if should_run:
        return condition.payload
    return None


def get_publish_payloads(action, device_payload):
    if action.payload:
        return (action.payload,)

    payloads = [get_condition_payload(condition, device_payload) for condition in action.actioncondition_set.all()]
    return (x for x in payloads if x is not None)


def publish(client, action, device_payload):
    payloads = get_publish_payloads(action, device_payload)
    for payload in payloads:
        for consumer in action.consumer_devices.all():
            client.publish(consumer.topic + '/set', json.dumps(payload))


def handle_action_device(client, device, msg):
    if not device.action_set:
        return

    for action in device.action_set.all():
        publish(client, action, json.loads(msg.payload.decode('utf-8')))


def handle_consumer_device(device, msg):
    if not msg.payload:
        return

    payload = msg.payload.decode('utf-8')
    try:
        device.state = json.loads(payload)
    except JSONDecodeError:
        device.state = {
            payload: payload,
        }
    device.save()


def handle_on_message(client, user_data, msg):
    topic = msg.topic
    action_devices = ActionDevice.objects.filter(topic=f'{topic}') \
        .prefetch_related("action_set") \
        .prefetch_related('action_set__consumer_devices') \
        .prefetch_related('action_set__actioncondition_set')

    for device in action_devices:
        handle_action_device(client, device, msg)

    consumer_devices = ConsumerDevice.objects.filter(topic=topic)

    for device in consumer_devices:
        handle_consumer_device(device, msg)


def register():
    mqtt_broker = "192.168.0.170"

    client = mqtt.Client("IoT Demo Client")
    client.connect(mqtt_broker)
    client.loop_start()

    client.subscribe("#")

    client.on_message = handle_on_message
    return client
