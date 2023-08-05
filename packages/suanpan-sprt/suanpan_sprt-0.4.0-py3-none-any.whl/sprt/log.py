import sys
import logging
from datetime import datetime, timezone
from urllib.parse import urljoin
from . import master, envs


class NodeStreamHandler(logging.StreamHandler):
    def __init__(self, stream=None):
        super().__init__()

    def get_stream(self):
        return sys.stdout

    def set_stream(self, _value):
        ...

    stream = property(get_stream, set_stream)


class LogkitHandler(logging.Handler):
    def __init__(self, uri, namespace, socketio_path, event):
        super().__init__()
        self.client = None
        self.uri = uri
        self.url = urljoin(uri, namespace)
        self.namespace = namespace
        self.socketio_path = socketio_path
        self.event = event

    def make_client(self):
        return master.sio(self.url, namespaces=self.namespace, socketio_path=self.socketio_path, wait_timeout=3)

    def send(self, msg):
        if not self.client:
            self.client = self.make_client()
        elif not self.client.connected:
            self.client.disconnect()
            self.client = self.make_client()
        self.client.emit(self.event, data=msg, namespace=self.namespace)

    @staticmethod
    def make_pickle(record):
        app = envs.appId
        extra = {"node": envs.nodeId}
        data = (app,
                {
                    "level": record.levelname,
                    "title": record.message,
                    "data": extra,
                    "time": datetime.now(timezone.utc).isoformat(),
                })
        return data

    def emit(self, record):
        if not self.uri:
            return

        try:
            msg = self.make_pickle(record)
            self.send(msg)
        except Exception:  # noqa
            self.handleError(record)

    def close(self):
        """
        Closes the socket.
        """
        self.acquire()
        try:
            client = self.client
            if client:
                self.client = None
                client.disconnect()
            super().close()
        finally:
            self.release()
