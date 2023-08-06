from typing import Mapping


def ensure_keys_match(*, expected: Mapping, actual: Mapping) -> None:
    if expected.keys() == actual.keys():
        return

    message = "expected keys to match but found:"

    missing_keys = expected.keys() - actual.keys()
    if len(missing_keys) > 0:
        message += f"\nmissing expected keys: {missing_keys}"

    unexpected_keys = actual.keys() - expected.keys()
    if len(unexpected_keys) > 0:
        message += f"\nunexpected keys: {unexpected_keys}"

    raise Exception(message)
