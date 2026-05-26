import os
import signal
import subprocess
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dashboard-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

process = None
process_lock = threading.Lock()


def stream_output(proc):
    try:
        for line in iter(proc.stdout.readline, b''):
            if proc.poll() is not None and not line:
                break
            text = line.decode('utf-8', errors='replace').rstrip('\n')
            if text:
                socketio.emit('log', {'data': text})
    except Exception as e:
        socketio.emit('log', {'data': f'[STREAM ERROR] {e}'})
    finally:
        proc.stdout.close()
        ret = proc.wait()
        socketio.emit('process_ended', {'code': ret})


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def on_connect():
    global process
    with process_lock:
        running = process is not None and process.poll() is None
    emit('status', {'running': running})


@socketio.on('ping_status')
def handle_ping():
    global process
    with process_lock:
        running = process is not None and process.poll() is None
    emit('status', {'running': running})


@socketio.on('start')
def handle_start():
    global process
    with process_lock:
        if process is not None and process.poll() is None:
            emit('log', {'data': '[DASHBOARD] Process sudah berjalan.'})
            return

        script_path = os.path.join(os.path.dirname(__file__), 'main.py')
        if not os.path.exists(script_path):
            emit('log', {'data': '[DASHBOARD] ERROR: main.py tidak ditemukan!'})
            emit('process_ended', {'code': -1})
            return

        try:
            process = subprocess.Popen(
                ['python', '-u', script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=os.path.dirname(__file__)
            )
            emit('log', {'data': f'[DASHBOARD] Process dimulai. PID: {process.pid}'})
            socketio.emit('status', {'running': True})

            t = threading.Thread(target=stream_output, args=(process,), daemon=True)
            t.start()
        except Exception as e:
            emit('log', {'data': f'[DASHBOARD] Gagal start: {e}'})
            emit('process_ended', {'code': -1})


@socketio.on('stop')
def handle_stop():
    global process
    with process_lock:
        if process is None or process.poll() is not None:
            emit('log', {'data': '[DASHBOARD] Tidak ada process yang berjalan.'})
            return
        try:
            os.kill(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
            emit('log', {'data': f'[DASHBOARD] Process dihentikan paksa. PID: {process.pid}'})
            socketio.emit('status', {'running': False})
        except Exception as e:
            emit('log', {'data': f'[DASHBOARD] Gagal stop: {e}'})


# Tidak pakai socketio.run() — Railway pakai gunicorn + eventlet
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
