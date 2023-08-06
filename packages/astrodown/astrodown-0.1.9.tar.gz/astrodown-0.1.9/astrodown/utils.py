from pathlib import Path


def file_ext(filename: str) -> str:
    return filename.split(".")[-1]


def enpath(path: str | Path) -> Path:
    return Path(path) if isinstance(path, str) else path
