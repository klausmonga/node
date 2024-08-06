import multiprocessing
from app.live.main import *
from lib.signalisation import *

def Oncreate():
    with open('lib/runtime_pid.bin', 'r') as outfile:
        try:
            local_data = json.loads(outfile.read())if outfile.read() else {'code_version': 0, 'pid': 0}
        except:
            local_data = {'code_version': 0, 'pid': 0}
    with open('lib/runtime_pid.bin', 'w') as outfile:
        json.dump({"pid": os.getpid(), "code_version": local_data['code_version']}, outfile)

    Onstart()

if __name__ == "__main__":
    runtime = multiprocessing.Process(name='runtime', target=Oncreate)
    signalisation = multiprocessing.Process(name='signalisation', target=run_signalisations)
    signalisation.start()
    runtime.start()