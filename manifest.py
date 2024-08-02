import time
import os
import json
import random
import multiprocessing
import time

def Onstart():
    b = 0
    while 1:
        print(b)
        time.sleep(1)
        random.random()
        b = random.randint(0, 50)
        os.system("/usr/bin/mosquitto_pub -h 127.0.0.1 -t ch1/temp -m " + str(b))

def signalisations():
    os.system("python3 /home/klaus/PycharmProjects/node/lib/signalisation.py")
def Oncreate():
    with open('lib/runtime_pid.bin', 'r') as outfile:
        local_data = json.loads(outfile.read())
    with open('lib/runtime_pid.bin', 'w') as outfile:
        json.dump({"pid": os.getpid(), "code_version": local_data['code_version']}, outfile)


    Onstart()


if __name__ == "__main__":
    runtime = multiprocessing.Process(name='runtime', target=Oncreate)
    signalisation = multiprocessing.Process(name='signalisation', target=signalisations)
    signalisation.start()
    runtime.start()