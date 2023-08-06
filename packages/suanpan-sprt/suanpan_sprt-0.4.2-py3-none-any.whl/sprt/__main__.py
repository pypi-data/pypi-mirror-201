import sys
import signal
import asyncio
import click
from hypercorn.asyncio import serve
from hypercorn.config import Config
from logging.config import dictConfig
from . import server, envs


@click.command()
@click.option('-h', '--host', default='localhost', envvar='RT_HOST', help='Runtime host')
@click.option('-p', '--port', default=9988, envvar='RT_PORT', help='Runtime port')
@click.option('-l', '--log-level', default='debug', envvar='RT_LOG_LEVEL', help='runtime logging level')
@click.option('-f', '--log-file', default='runtime.log', envvar='RT_LOG_FILE', help='runtime logging file')
@click.option('-w', '--working-dir', default='.', envvar='RT_WORKING_DIR', help='working dir')
def main(host, port, log_level: str, log_file: str, working_dir: str):
    if log_level.upper() in ('CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG'):
        dictConfig({
            'version': 1,
            'root': {
                'level': log_level.upper(),
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
                    'filename': log_file,
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
                    'level': log_level.upper(),
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

    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGINT, receive_signal)
    app = server.create_app(working_dir, log_file)

    config = Config()
    config.bind = [f'{host}:{port}']
    app.logger.info(f'python runtime running on {host}:{port}')
    asyncio.run(serve(app, config))


def receive_signal(signal_number, frame):
    print('receive_signal', signal_number)
    sys.exit(128 + signal_number)


if __name__ == '__main__':
    main()
