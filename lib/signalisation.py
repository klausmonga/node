# python 3.11
import os
import random
import json
from paho.mqtt import client as mqtt_client
import time
import git  # pip install gitpython
from git import RemoteProgress
from lib.signal_msg import send_report

broker = '127.0.0.1'
port = 1883
topic = "iot/signalisations"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1,client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        with open('lib/runtime_pid.bin', 'r') as outfile:
            local_data = json.loads(outfile.read())
            remote_data = json.loads(str(msg.payload.decode()))
            if local_data['code_version'] < remote_data['code_version']:
            # start git pull
                git.Repo.clone_from(remote_data['code_url'], 'staging/staging-'+str(remote_data['code_version'])+"/",
                                branch='main', progress=CloneProgress())
                print('Cloned!')
                #start test
                os.system("python3 "+"staging/staging-"+str(remote_data['code_version'])+"/live_tests/tests.py")
                print("end signal!!!")
            else:
                send_report({
                    "status": 2,
                    "message": "THE LIVE CODE IS UPDATED !!!"
                })
            # os.kill(json.loads(outfile.read())['pid'],1)


    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
