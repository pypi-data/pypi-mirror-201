import logging
from typing import List
import requests

from .exceptions import APIException
from .secrets import get_secret

logger = logging.getLogger(__name__)

PRESIGN_URL_NAME = 'presign_url'
HTTP_TOKEN_NAME = 'http_token'


class RecordingFetcher(object):
    def __init__(self, secret_name: str):
        self.secret_name = secret_name
        self._secrets = get_secret(self.secret_name)

    def get_secret(self, key: str):
        try:
            return self._secrets[key]
        except KeyError:
            raise KeyError(f'Key {key} not found in secret {self.secret_name}')

    def get(self, bucket: str, key: str) -> str:
        """
        Get presigned url for a single S3 object

        :param bucket: S3 bucket name
        :param key: S3 object key
        :return: presigned url, a long string
        :raises: APIException
        """
        if isinstance(key, list):
            raise ValueError("key must be a string")

        presign_url = self.get_secret(PRESIGN_URL_NAME)
        token = self.get_secret(HTTP_TOKEN_NAME)
        response = requests.post(presign_url, headers={'Authorization': token}, json={
            'bucket': bucket,
            'keys': [key],
        })
        if response.ok:
            return response.json()[0]
        else:
            msg = f'Failed to get presigned url for {bucket}/{key}. response: HTTP {response.status_code} content:{response.text}'
            logger.debug(msg)
            raise APIException(msg)
            

    def get_multi(self, bucket: str, keys: List[str]) -> List[str]:
        """
        GEt presigned url for multiple S3 objects

        :param bucket: S3 bucket name
        :param keys: List of S3 object keys
        :return: list of presigned urls
        :raises: APIException
        """
        presign_url = self.get_secret(PRESIGN_URL_NAME)
        token = self.get_secret(HTTP_TOKEN_NAME)
        response = requests.post(presign_url, headers={'Authorization': token}, json={
            'bucket': bucket,
            'keys': keys,
        })
        if response.ok:
            return response.json()
        else:
            msg = f'Failed to get presigned url for {bucket}/{keys}. response: HTTP {response.status_code} content:{response.text}'
            logger.debug(msg)
            raise APIException(msg)
