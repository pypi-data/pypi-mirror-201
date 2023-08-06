import os
from typing import Optional


def get_optional_string_env(name: str) -> Optional[str]:
    value = os.getenv(key=name)
    if value is None or len(value) == 0:
        return None

    return value


def get_optional_int_env(name: str) -> Optional[int]:
    value = get_optional_string_env(name)
    if value is None:
        return None

    return int(value)


def get_required_string_env(name: str) -> str:
    value = get_optional_string_env(name)
    if value is None:
        raise Exception(f"missing required env variable: {name}")

    return value


def get_required_int_env(name: str) -> int:
    value = get_optional_int_env(name)
    if value is None:
        raise Exception(f"missing required env variable: {name}")

    return value
