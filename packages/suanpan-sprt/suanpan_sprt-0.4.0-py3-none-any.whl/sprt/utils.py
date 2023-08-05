import os
import hashlib
import base64


def safe_mkdirs(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
    return path


def safe_mkdirs_for_file(filepath):
    return safe_mkdirs(os.path.dirname(os.path.abspath(filepath)))


def md5(filepath, block_size=64 * 1024):
    with open(filepath, "rb") as f:
        _md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            _md5.update(data)
    return base64.b64encode(_md5.digest()).decode()
