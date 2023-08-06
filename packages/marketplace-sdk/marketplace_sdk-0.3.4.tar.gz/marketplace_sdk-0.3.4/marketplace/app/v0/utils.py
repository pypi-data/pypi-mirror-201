import json
import re


def _encode_metadata(metadata: dict = None) -> dict:
    return {
        f"X-Object-Meta-{name}": json.dumps(value) for name, value in metadata.items()
    }


def _decode_metadata(headers: dict = None) -> dict:
    return {
        re.sub(r"^X-Object-Meta-", "", name): json.loads(value)
        for name, value in headers.items()
        if str(name).startswith("X-Object-Meta-")
    }
