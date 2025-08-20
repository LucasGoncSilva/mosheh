from collections.abc import Generator
from hashlib import sha256
from itertools import compress, product
from typing import Any, Final

from account.models import ActivationAccountToken, User
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


SK: Final[str] = settings.SECRET_KEY


def xor(token: str, key: str, encrypt: bool = True) -> str:
    if token is None or not isinstance(token, str) or not len(key):
        return token

    # Calculate the necessary key repetitions
    key_repetitions: int = max(1, (len(token) + len(key) - 1) // len(key))

    # Expand the key and secret key to match the token length
    expanded_key: str = (key * key_repetitions)[: len(token)]
    expanded_secret_key: str = (SK * key_repetitions)[: len(token)]

    # Create a generator for XORed values
    xor_key_generator: Generator = (
        ord(expanded_key_char) ^ ord(secret_key_char)
        for expanded_key_char, secret_key_char in zip(expanded_key, expanded_secret_key)
    )

    # Encrypt or decrypt the token
    if encrypt:
        transformed_chars: list[str] = [
            chr((ord(text_char) ^ xor_key_val) + 32)
            for text_char, xor_key_val in zip(token, xor_key_generator)
        ]
    else:
        transformed_chars: list[str] = [
            chr((ord(text_char) - 32) ^ xor_key_val)
            for text_char, xor_key_val in zip(token, xor_key_generator)
        ]

    return ''.join(transformed_chars)


def uidb64(uuid: str) -> str:
    return urlsafe_base64_encode(force_bytes(uuid))


def create_activation_account_token(new_user: User) -> ActivationAccountToken:
    token_hash: str = sha256(
        f'{new_user.username}{new_user.password}'.encode()
    ).hexdigest()

    token: ActivationAccountToken = ActivationAccountToken.objects.create(
        value=token_hash,
        user=new_user,
        used=False,
    )

    token.full_clean()

    return token


def create_scenarios(params: list[dict[str, Any]]) -> Generator:
    for case in product([0, 1], repeat=len(params)):
        if all(case):
            break
        _temp: compress[dict[str, Any]] = compress(params, case)
        temp: list[dict[str, Any]] = list(_temp)
        scenario: dict = {}

        for param in temp:
            scenario.update(param)

        yield case, scenario
