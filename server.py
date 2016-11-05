#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import logging
import sillygames.app
from flask import jsonify

async_mode = None
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
# app._static_folder='.'


class SocketIOHandler(logging.Handler):
    """
    A handler class which writes logging records, appropriately formatted,
    to a stream. Note that this class does not close the stream, as
    sys.stdout or sys.stderr may be used.
    """

    def __init__(self):
        """
        Initialize the handler.
        If stream is not specified, sys.stderr is used.
        """
        logging.Handler.__init__(self)
        # if stream is None:
        #     stream = sys.stderr
        # self.stream = stream

    def flush(self):
        """
        Flushes the stream.
        """
        self.acquire()
        try:
            pass
            # print("flushed")
            # if self.stream and hasattr(self.stream, "flush"):
            #     self.stream.flush()
        finally:
            self.release()

    def emit(self, record):
        """
        Emit a record.
        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        try:
            if record.name == 'werkzeug':
                return

            msg = self.format(record)
            socketio.emit('log',
                          {'data': msg})
            # stream = self.stream
            # stream.write(msg)
            # stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

    def __repr__(self):
        level = getLevelName(self.level)
        # name = getattr(self.stream, 'name', '')
        name = "SocketIOHandler"
        if name:
            name += ' '
        return '<%s %s(%s)>' % (self.__class__.__name__, name, level)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
sh = SocketIOHandler()
ch = logging.StreamHandler()
logger.addHandler(sh)
logger.addHandler(ch)

def app_thread():
    """Example of how to send server generated events to clients."""
    socketio.emit('status', {'running': False}, broadcast=True)
    try:
        sillygames.app.main(callback=lambda: socketio.emit('status', {'running': True}, broadcast=True))
        socketio.emit('status', {'running': False, 'error': 'not running'}, broadcast=True)
    except Exception as e:
        socketio.emit('status', {'running': False, 'error': str(e)}, broadcast=True)
        logger.error(e)
    finally:
        global thread
        thread = None

@socketio.on('connect')
def connect():
    emit('log', {'data': 'Connected to log', 'count': 0})


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected', request.sid)
    
@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/start')
def start():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=app_thread)
    return jsonify(success=True)

@app.route('/status')
def status():
    global thread
    return jsonify(running=(not thread is None), error='not running')

@app.route('/commands')
def commands():
    return jsonify(sillygames.app.availableCommands())
    

if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=5000, debug=True)
    
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)