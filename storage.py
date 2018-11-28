from hashlib import md5
from pathlib import Path
from re import compile


def save(file_bytes):
    file_hash = md5(file_bytes).hexdigest()
    folder = Path(f'store/{file_hash[:2]}')
    folder.mkdir(parents=True, exist_ok=True)
    file = folder / file_hash
    file.write_bytes(file_bytes)
    return file_hash


def get_path(hash):
    file = Path(f'store/{hash[:2]}/{hash}')
    if file.exists():
        return file
    else:
        raise FileNotFoundError()


def delete(hash):
    file = get_path(hash)
    file.unlink()


hash_symbols = compile('^[0-9a-f]+$')


def valid_hash(hash):
    return bool(hash_symbols.match(hash))
