# python 3.11
import os
import sys
import multiprocessing
import random
import json
from paho.mqtt import client as mqtt_client
import run
import time
import git  # pip install gitpython
from git import RemoteProgress

broker = '127.0.0.1'
port = 1883
topic = "iot/signalisations/report"
# Generate a Client ID with the subscribe prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'
FLAG = False

def init_test(status):
    FLAG = status

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
def reload_runtime():
    os.system("python3 run.py")
# mosquitto_pub -h 127.0.0.1 -t iot/signalisations -m '{"code_version":2, "code_url": "git@github.com:klausmonga/node.git"}'
def publish(client,report):
        if report['status'] == 1:
            print("FLAG:: " + str(report['flag']))
            if report['flag']:
                print("IN..XXXXXXX...")
                with open('lib/runtime_pid.bin', 'r') as outfile:
                    local_data = json.loads(outfile.read())
                    print("killing runtime "+str(local_data['pid']))
                    os.kill(local_data['pid'],1)
                os.system("mv app/live app/live-old-"+sys.argv[1])
                os.system("mv app/staging_app_"+sys.argv[1]+" app/live")
                runtime = multiprocessing.Process(name='runtime', target=reload_runtime)
                runtime.start()
        result = client.publish(topic, json.dumps(report))
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
