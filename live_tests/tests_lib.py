# python 3.11
import os
import random
import json
from paho.mqtt import client as mqtt_client
import time
import git  # pip install gitpython
from git import RemoteProgress

broker = '127.0.0.1'
port = 1883
topic = "iot/signalisations/staging"
# Generate a Client ID with the subscribe prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'
NB_TESTS = 0
COUNTER = 0
def init_test(nb_test):
    NB_TESTS = nb_test

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

def publish(client,report):
        if json.loads(report)['status'] == 1:
            COUNTER =+ 1
            if NB_TESTS == COUNTER:
                with open('lib/runtime_pid.bin', 'r') as outfile:
                    local_data = json.loads(outfile.read())
                    os.kill(local_data['pid'],1)
        result = client.publish(topic, report)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{report}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")


def send_report(report):
    client = connect_mqtt()
    client.loop_start()
    publish(client, report)
    client.loop_stop()

#
# if __name__ == '__main__':
#     run()
