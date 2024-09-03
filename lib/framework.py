# python 3.11
import os
import random
import multiprocessing
import json
from paho.mqtt import client as mqtt_client
import time
import git  # pip install gitpython
from git import RemoteProgress
from lib.signal_msg import send_report

broker = '127.0.0.1'
port = 1883
topic = "iot/signalisations/framework"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("FRAMEWORK Connected to MQTT Broker!")
        else:
            print("FRAMEWORK Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1,client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)
def reload_runtime():
    os.system("python3 run.py")
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        with open('app/live/manifest.json', 'r') as outfile:
            local_data = json.loads(outfile.read())
            remote_data = json.loads(str(msg.payload.decode()))
            local_data['remote_params'] = remote_data
            with open('app/live/manifest.json', 'w') as outfile:
                json.dump(local_data, outfile)
            with open('lib/runtime_pid.bin', 'r') as outfile:
                local_data = json.loads(outfile.read())
                print("killing runtime " + str(local_data['pid']))
                os.kill(local_data['pid'], 1)
            print("reloading runtime!!!")
            runtime = multiprocessing.Process(name='runtime', target=reload_runtime)
            runtime.start()


            # os.kill(json.loads(outfile.read())['pid'],1)


    client.subscribe(topic)
    client.on_message = on_message


def run_framework():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

