import hashlib


def calc_queue_name(application_id: str, application_secret: str) -> str:
    h = int(
        hashlib.sha256(
            (application_id + application_secret).encode("utf-8")
        ).hexdigest(),
        16,
    ) % (10**16)
    return f"{application_id}:{h}"
