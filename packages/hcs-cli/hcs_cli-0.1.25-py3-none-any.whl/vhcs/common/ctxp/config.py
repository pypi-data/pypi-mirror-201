from .jsondot import dotdict
from .fstore import fstore

_store_impl: fstore = None


def _init(config_path: str) -> None:
    global _store_impl
    _store_impl = fstore(config_path)


def get(name: str, reload: bool = False) -> dotdict:
    return _store_impl.get(name, reload)


def list() -> list[str]:
    return _store_impl.keys()
