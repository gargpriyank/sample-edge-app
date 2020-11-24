import paho.mqtt.client as mqtt
import base64 
import json
import os
import subprocess

DATA_TOPIC = "local/esf/opcua/data"
STATISTICS_TOPIC = "local/esf/opcua/statistics"
HOST = "esf-ieam"
PORT = 1883
OBSERVED_DATA = set([ "buzzer", "led", "fan", "light", "temperature" ])
ES_BROKER_URL = os.environ["EVENTSTREAMS_BROKER_URL"]
ES_API_KEY = os.environ["EVENTSTREAMS_API_KEY"]
ES_TOPIC_NAME = os.environ["EVENTSTREAMS_TOPIC_NAME"]

class EdgeApp:

    def __init__(self, keys_to_observe):
        self.keys_to_observe = keys_to_observe
        # initialize the internal matematical structures
        self.sum = dict()
        self.squared_sum = dict()
        self.count = dict()
        self.min = dict()
        self.max = dict()
        self.count = dict()
        self.reset()

    def reset(self):
        for key in self.keys_to_observe:
            self.sum[key] = 0
            self.squared_sum[key] = 0
            self.count[key] = 0
            self.min[key] = float('inf')
            self.max[key] = float('-inf')

    def get_statistics(self, new_data):
        statistics = dict()
        for key in new_data:
            if key in self.keys_to_observe:
                self.sum[key] += new_data[key]
                self.squared_sum[key] += new_data[key] * new_data[key]
                self.count[key] += 1
                statistics[key + "_avg"] = self.get_avg_(key)
                statistics[key + "_min"] = self.get_min_(key, new_data[key])
                statistics[key + "_max"] = self.get_max_(key, new_data[key])
                statistics[key + "_std"] = self.get_std_(key)
        
        return statistics

    def get_avg_(self, key):
        return self.sum[key] / self.count[key]

    def get_min_(self, key, new_data):
        if self.min[key] > new_data:
            self.min[key] = new_data
        return self.min[key]
    
    def get_max_(self, key, new_data):
        if self.max[key] < new_data:
            self.max[key] = new_data
        return self.max[key]
    
    def get_std_(self, key):
        key_avg = self.get_avg_(key)
        return self.squared_sum[key] - self.count[key] * key_avg * key_avg


def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    new_data = json.loads(message.payload.decode("utf-8"))["metrics"]
    message = dict()
    message["metrics"] = edge_app.get_statistics(new_data)
    send(message)

def send(message):
    print("sending message: " + json.dumps(message))
    client.publish(STATISTICS_TOPIC, json.dumps(message))
    publish_cmd = "echo " + json.dumps(message) + " | kafkacat -P -b " + ES_BROKER_URL + " -X api.version.request=true -X " \
    "security.protocol=sasl_ssl -X sasl.mechanisms=PLAIN -X sasl.username=token -X sasl.password=" + ES_API_KEY + " -t " + ES_TOPIC_NAME
    print(publish_cmd)
    os.system(publish_cmd)

def on_log(client, userdata, level, buf):
    print("log: ", buf)

def on_connect(client, userdata, flags, rc):
    print("Subscribing to topic", DATA_TOPIC)
    client.subscribe(DATA_TOPIC)

edge_app = EdgeApp(OBSERVED_DATA)

client = mqtt.Client("mqtt_app", clean_session=False)
client.username_pw_set(username="mqtt", password="mqtt")
client.on_message=on_message
client.on_log=on_log
client.on_connect=on_connect
client.connect(HOST, port=PORT)

client.loop_forever()