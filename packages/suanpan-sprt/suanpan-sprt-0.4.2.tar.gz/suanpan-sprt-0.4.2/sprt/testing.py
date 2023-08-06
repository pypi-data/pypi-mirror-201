import sys
import uuid
import json
from logging.config import dictConfig
from . import envs


class TestNode(object):
    def __init__(self, working_dir, file, function='main'):
        self.id = uuid.uuid4().hex
        self.file = file
        self.working_dir = working_dir
        self.function = function
        self.params = {}
        self.node_id = 'test_node'

        dictConfig({
            'version': 1,
            'root': {
                'level': 'DEBUG',
                'handlers': ['console']
            },
            'handlers': {
                'console': {
                    'class': 'sprt.log.NodeStreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'std_out',
                    'stream': sys.stdout
                },
                'rotate_file': {
                    'level': 'DEBUG',
                    'formatter': 'std_out',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': 'sprt.server.log',
                    'encoding': 'utf8',
                    'maxBytes': 10000000,
                    'backupCount': 1,
                },
                'logkit': {
                    'class': 'sprt.log.LogkitHandler',
                    'level': 'INFO',
                    'uri': envs.logkitUri,
                    'namespace': envs.logkitNamespace,
                    'socketio_path': envs.logkitPath,
                    'event': envs.logkitEventsAppend
                }
            },
            'formatters': {
                'std_out': {
                    'format': '%(asctime)s :: [%(levelname)-8s] %(message)s',
                    # 'datefmt': '%Y-%m-%d %H:%M:%S'
                },
            },
            'loggers': {
                'sprt.server': {
                    'level': 'DEBUG',
                    'handlers': ['rotate_file'],
                    'propagate': False
                },
                'logkit': {
                    'level': envs.logkitLogsLevel.upper(),
                    'handlers': ['console', 'logkit'],
                    'propagate': False
                }
            },
        })

    def set_params(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, str):
                v = {"type": "string", "value": value}
            elif isinstance(value, (int, float, complex)):
                v = {"type": "number", "value": value}
            elif isinstance(value, list):
                v = {"type": "array", "value": json.dumps(value)}
            elif isinstance(value, dict):
                v = {"type": "json", "value": json.dumps(value)}
            else:
                v = {"type": "all", "value": str(value)}
            self.params[key] = v

    @staticmethod
    def _dumps(value):
        if isinstance(value, dict) or isinstance(value, list):
            value = json.dumps(value)

        return value

    def get_request(self, *args):
        _args = {f'in{index + 1}': self._dumps(arg) for index, arg in enumerate(args)}
        ret = {
            'id': self.id,
            'file': self.file,
            'working_dir': self.working_dir,
            'function': self.function,
            'context': {
                'request_id': uuid.uuid4().hex,
                'node_id': self.node_id,
                'params': self.params,
                'args': _args
            }
        }
        return ret
