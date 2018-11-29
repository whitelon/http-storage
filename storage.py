from pathlib import Path
from re import compile


def move(tempfile, file_hash):
    folder = Path(f'store/{file_hash[:2]}')
    folder.mkdir(parents=True, exist_ok=True)
    file = folder / file_hash
    tempfile.replace(file)
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
