import os
import abc
import logging
import pathlib
import functools
import minio
from . import master, envs, utils

logger = logging.getLogger('logkit')


class Storage(abc.ABC):
    CONTENT_MD5 = "Content-MD5"
    _instance = None

    def __init__(self, endpoint, bucket, access_id, access_secret, root_path='', temp_store='', global_store=''):
        self.endpoint = endpoint
        self.bucket = bucket
        self.access_id = access_id
        self.access_secret = access_secret
        self.root_path = root_path
        self.temp_store = temp_store
        self.global_store = global_store

    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance

        if envs.storageType == 'oss':
            cls._instance = OssStorage(
                envs.storageEndpoint, envs.storageBucket,
                envs.storageAccessId, envs.storageAccessSecret,
                envs.storageRootPath, envs.storageTempStore, envs.storageGlobalStore
            )
        elif envs.storageType == 'minio':
            cls._instance = MinioStorage(
                envs.storageEndpoint, envs.storageBucket,
                envs.storageAccessId, envs.storageAccessSecret,
                envs.storageRootPath, envs.storageTempStore, envs.storageGlobalStore
            )
        else:
            return None

        return cls._instance

    @abc.abstractmethod
    def download(self, key, path=None, **kwargs):
        pass

    @abc.abstractmethod
    def upload(self, key, path, **kwargs):
        pass

    @abc.abstractmethod
    def copy(self, key, dist, progress=None, **kwargs):
        pass

    @abc.abstractmethod
    def remove(self, key, progress=None, **kwargs):
        pass

    def local_temp_path(self, *path):
        if self.root_path:
            tmp = pathlib.Path(self.root_path) / envs.userId / envs.appId / envs.nodeId / self.temp_store.lstrip('/')
        else:
            tmp = pathlib.Path(self.temp_store)

        p = tmp.joinpath(*path).resolve()
        path = str(p)
        if isinstance(p, pathlib.WindowsPath):
            if len(path) > 200:
                path = "\\\\?\\" + str(p)
        return path

    @abc.abstractmethod
    def get_storage_md5(self, name, **kwargs):
        pass

    @staticmethod
    def get_local_md5(path):
        return utils.md5(path) if os.path.isfile(path) else None

    @staticmethod
    def check_md5(md5a, md5b):
        return md5a if md5a == md5b and md5a is not None else False

    @property
    def node_data_store_key(self):
        return pathlib.PurePosixPath("studio", envs.userId, "share", envs.appId, envs.nodeId)

    def get_key_in_node_data_store(self, *paths):
        return str(self.node_data_store_key.joinpath(*paths))


class MinioStorage(Storage):
    def __init__(self, endpoint, bucket, access_id, access_secret,
                 root_path='', temp_store='', global_store='', secure=True):
        endpoint, secure = self._analyze_endpoint(endpoint, secure)
        super().__init__(
            endpoint, bucket, access_id, access_secret,
            root_path=root_path, temp_store=temp_store, global_store=global_store
        )
        self.secure = secure
        self.client = self._connect_client(access_id, access_secret)

    @staticmethod
    def _analyze_endpoint(endpoint, secure=False):
        https_prefix = "https://"
        if endpoint.startswith(https_prefix):
            return endpoint[len(https_prefix):], True

        http_prefix = "http://"
        if endpoint.startswith(http_prefix):
            return endpoint[len(http_prefix):], False

        return endpoint, secure

    def _connect_client(self, access_id=None, access_secret=None):
        if access_id and access_secret:
            self.access_id = access_id
            self.access_secret = access_secret
        else:
            data = master.get_token()
            self.access_id = data["Credentials"]["AccessKeyId"]
            self.access_secret = data["Credentials"]["AccessKeySecret"]

        client = minio.Minio(
            self.endpoint,
            access_key=self.access_id,
            secret_key=self.access_secret,
            secure=self.secure,
        )
        return client

    def auto_refresh_token(self, func):
        @functools.wraps(func)
        def _dec(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except minio.error.S3Error as e:
                if e.code == "AccessDenied":
                    logger.warning("Minio access denied, refreshing access key.")
                    self.client = self._connect_client()
                    return func(*args, **kwargs)
                raise e

        return _dec

    def download(self, key, path=None, bucket=None):
        bucket = bucket or self.bucket
        path = pathlib.Path(path) if path else self.local_temp_path(key)

        object_md5 = self.get_storage_md5(key, bucket=bucket)
        file_md5 = self.get_local_md5(path)
        if self.check_md5(object_md5, file_md5):
            return path

        utils.safe_mkdirs_for_file(path)
        self.auto_refresh_token(self.client.fget_object)(bucket, key, path)
        return path

    def upload(self, key, path, bucket=None):
        bucket = bucket or self.bucket
        path = pathlib.Path(path).resolve()

        object_md5 = self.get_storage_md5(key, bucket=bucket)
        file_md5 = self.get_local_md5(path)
        if self.check_md5(object_md5, file_md5):
            return path

        self.auto_refresh_token(self.client.fput_object)(bucket, key, path)
        return path

    def copy(self, key, dist, progress=None, **kwargs):
        pass

    def remove(self, key, progress=None, **kwargs):
        pass

    def get_storage_md5(self, name, **kwargs):
        return ''


class OssStorage(Storage):
    def __init__(self, endpoint, bucket, access_id, access_secret, root_path='', temp_store='', global_store=''):
        super().__init__(
            endpoint, bucket, access_id, access_secret,
            root_path=root_path, temp_store=temp_store, global_store=global_store
        )

    def download(self, key, path=None, bucket=None):
        pass

    def upload(self, key, path, bucket=None):
        pass

    def copy(self, key, dist, progress=None, **kwargs):
        pass

    def remove(self, key, progress=None, **kwargs):
        pass

    def get_storage_md5(self, name, **kwargs):
        return ''
