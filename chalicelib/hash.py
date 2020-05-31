import hashlib


def md5_checksum(file_bytes: bytes) -> str:
    return hashlib.md5(file_bytes).hexdigest()
