import base64
import hashlib
import hmac
import socketio
from . import envs


def encode(data):
    if isinstance(data, str):
        data = data.encode()
    return data


def decode(data):
    if isinstance(data, bytes):
        data = data.decode()
    return data


def signature_v1(secret, data):
    h = hmac.new(encode(secret), encode(data), hashlib.sha1)
    return decode(base64.b64encode(encode(h.digest())))


def default_headers():
    return {
        envs.userIdHeaderField: envs.userId,
        envs.userSignatureHeaderField: signature_v1(envs.accessSecret, envs.userId),
        envs.userSignVersionHeaderField: "v1",
    }


def sio(*args, **kwargs):
    kwargs["headers"] = {**default_headers(), **kwargs.pop("headers", {})}
    client = socketio.Client()
    client.connect(*args, **kwargs)

    return client


def get_token():
    # TODO: add for oss
    ...
