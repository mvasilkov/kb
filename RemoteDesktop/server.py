#!/usr/bin/env python
import ctypes
from flask import Flask, request, send_file
from PIL import ImageGrab
from StringIO import StringIO

# http://msdn.microsoft.com/en-us/library/windows/desktop/ms646260%28v=vs.85%29.aspx
MOUSEEVENTF_LEFTDOWN = 2
MOUSEEVENTF_LEFTUP = 4

app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/desktop.jpeg')
def desktop():
    screen = ImageGrab.grab()
    buf = StringIO()
    screen.save(buf, 'JPEG', quality=75)
    buf.seek(0)
    return send_file(buf, mimetype='image/jpeg')


@app.route('/click')
def click():
    try:
        x = int(request.args.get('x'))
        y = int(request.args.get('y'))
    except:
        return 'error'
    user32 = ctypes.windll.user32
    user32.SetCursorPos(x, y)
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    return 'done'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7080, debug=True)
