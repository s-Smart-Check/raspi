import subprocess
import os
import signal
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)
stream_process = None

def signal_handler(sig, frame):
    print('all process stop')
    global stream_process
    if stream_process is not None and stream_process.poll() is None:
        stream_process.terminate()
        stream_process.wait()
    sys.exit(0)

@app.route('/start', methods=['GET'])
def start_stream():
    global stream_process
    if stream_process is None or stream_process.poll() is not None:
        stream_process = subprocess.Popen(["python", "streaming.py"])
        return "streaming started"
    else:
        return "streaming is already running"

@app.route('/stop', methods=['GET'])
def stop_stream():
    global stream_process
    if stream_process is not None and stream_process.poll() is None:
        stream_process.terminate()
        return "streaming stopped"
    else:
        return "Face recognition is not running"

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
