from base64 import b64decode, b64encode
from functools import lru_cache
from json import dumps, loads
from os import getenv, urandom
from random import choices
from string import ascii_letters, digits
from typing import Any, Self, TypedDict, cast
from zlib import compress, decompress

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from django.conf import settings
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import CharField, TextField
from django.db.models.expressions import Expression


class PayloadV1(TypedDict):
    version: int
    time_cost: int
    memory_cost: int
    parallelism: int
    nonce: str
    ciphertext: str


class sWardenCryptography:
    DEFAULT_TC: int
    DEFAULT_MC: int
    DEFAULT_P: int
    _DEFAULT_VALUES: str = getenv('DEFAULT_TC_MC_P', '6,131072,1')

    try:
        DEFAULT_TC, DEFAULT_MC, DEFAULT_P = map(int, _DEFAULT_VALUES.split(','))
    except ValueError:
        DEFAULT_TC, DEFAULT_MC, DEFAULT_P = 6, 131072, 1

    @classmethod
    @lru_cache
    def _derive_key(cls, key1: str, key2: str, tc: int, mc: int, p: int) -> bytes:
        return hash_secret_raw(
            secret=key1.encode(),
            salt=key2.encode(),
            time_cost=tc,
            memory_cost=mc,
            parallelism=p,
            hash_len=32,
            type=Type.ID,
        )

    @classmethod
    def encrypt(
        cls,
        plaintext: str,
        key1: str,
        key2: str,
        tc: int = DEFAULT_TC,
        mc: int = DEFAULT_MC,
        p: int = DEFAULT_P,
    ) -> str:
        compressed_data: bytes = compress(plaintext.encode())

        key: bytes = cls._derive_key(key1, key2, tc, mc, p)
        aesgcm: AESGCM = AESGCM(key)
        nonce: bytes = urandom(12)
        ciphertext: bytes = aesgcm.encrypt(nonce, compressed_data, None)

        payload: PayloadV1 = {
            'version': 1,
            'time_cost': tc,
            'memory_cost': mc,
            'parallelism': p,
            'nonce': b64encode(nonce).decode(),
            'ciphertext': b64encode(ciphertext).decode(),
        }

        return b64encode(dumps(payload).encode()).decode()

    @classmethod
    def decrypt(cls, token_b64: str, key1: str, key2: str) -> str:
        try:
            decoded: bytes = b64decode(token_b64)
            payload: PayloadV1 = loads(decoded.decode())
        except Exception as e:
            raise ValueError(f'Invalid token: {e}')

        if payload.get('version') == 1:
            return cls._decrypt_v1(payload, key1, key2)
        else:
            raise ValueError(f'Unsupported payload version: {payload.get("v")}')

    @classmethod
    def _decrypt_v1(cls, payload: PayloadV1, key1: str, key2: str) -> str:
        for info in ('time_cost', 'memory_cost', 'parallelism', 'nonce', 'ciphertext'):
            if info not in payload:
                raise ValueError(f'Payload require field {info}')

        tc: int = int(payload['time_cost'])
        mc: int = int(payload['memory_cost'])
        p: int = int(payload['parallelism'])
        nonce: bytes = b64decode(str(payload['nonce']))
        ciphertext: bytes = b64decode(str(payload['ciphertext']))

        key: bytes = cls._derive_key(key1, key2, tc, mc, p)
        aesgcm: AESGCM = AESGCM(key)
        plaintext: bytes = aesgcm.decrypt(nonce, ciphertext, None)
        decompressed_data: bytes = decompress(plaintext)
        return decompressed_data.decode()


class EncryptedFieldMixin:
    def __init__(
        self,
        *args: Any,
        key1: str | None = None,
        key2: str = settings.SECRET_KEY,
        **kwargs: Any,
    ) -> None:
        self.key1: str = key1 or ''.join(choices(ascii_letters + digits, k=128))
        self.key2: str = key2

        return super().__init__(*args, **kwargs)

    def get_prep_value(self, value: Any) -> str:
        if value:
            return sWardenCryptography.encrypt(str(value), self.key1, self.key2)
        return value

    def from_db_value(
        self, value: Any, expression: Expression, connection: BaseDatabaseWrapper
    ) -> str:
        if value:
            return sWardenCryptography.decrypt(str(value), self.key1, self.key2)
        return value


class EncryptedCharField(EncryptedFieldMixin, CharField):
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        return cast(Self, super().__new__(cls))


class EncryptedTextField(EncryptedFieldMixin, TextField):
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        return cast(Self, super().__new__(cls))
