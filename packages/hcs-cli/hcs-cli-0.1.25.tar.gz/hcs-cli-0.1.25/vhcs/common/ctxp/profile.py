from .util import CtxpException
from .jsondot import dotdict
from .fstore import fstore


_store: fstore = None
_active_profile_name: str = None
_plain: dotdict = None

_active_profile_store_item = ".active"


def init(repo_path: str, active_profile_name: str = None) -> None:
    global _store, _active_profile_name
    _store = fstore(repo_path)
    if active_profile_name:
        _active_profile_name = active_profile_name


def path() -> str:
    """Get directory name of the current active profile"""
    active_profile = name()
    if not active_profile:
        return None
    return _store._get_path(active_profile)


def create(name: str, data: dict) -> None:
    _store.save(name, data)
    use(name)


def current(reload: bool = False) -> dict:
    """Get content of the current active profile"""
    profile_name = name()
    if not profile_name:
        raise CtxpException("Profile not specified")
    data = get(profile_name, reload)
    global _plain
    _plain = None
    return data


def name() -> str:
    """Get the current active profile name"""

    global _active_profile_name
    if not _active_profile_name:
        # Try load from "default"
        _active_profile_name = _store.get(key=_active_profile_store_item, format="text")
        if not _active_profile_name:
            # If only one profile, use it
            names = list()
            if len(names) == 1:
                _active_profile_name = names[0]
    return _active_profile_name


def use(name: str) -> str:
    """Use to the specified profile"""

    global _active_profile_name, _plain

    if _active_profile_name == name:
        return name

    profile_exists = _store.contains(name)
    if not profile_exists:
        return

    _plain = None
    _active_profile_name = name
    _store.save(_active_profile_store_item, name)
    return name


def list() -> list[str]:
    """List profile names"""
    names = _store.keys()
    try:
        names.remove(_active_profile_store_item)
    except:
        pass
    return names


def delete(profile_name: str = None) -> None:
    """Delete a profile"""

    # delete associated context
    from . import context

    context.destroy(profile_name)

    if profile_name is None:
        profile_name = name()
    global _active_profile_name, _plain
    if _active_profile_name == profile_name:
        _active_profile_name = None
        _plain = None
    _store.delete(profile_name)


def get(name: str, reload: bool = False, default=None) -> dotdict:
    """Get profile data by name"""
    data = _store.get(key=name, reload=reload, default=default)
    if data:
        data["_profile_name"] = name
    return data


def file(name: str) -> str:
    """Get the file path of a profile"""
    return _store._get_path(name)


def exists(name: str) -> bool:
    return _store.contains(name)


# --------------------------------------------------


def _nested_obj_to_plain_dict(obj: any, path: str, result: dotdict) -> None:
    t = type(obj)
    if t is str or t is int or t is float or t is bool:
        result[path] = obj
    elif t is dict or t is dotdict:
        for k in obj:
            v = obj[k]
            _nested_obj_to_plain_dict(v, path + "." + k, result)
    elif t is list:
        for i in range(len(obj)):
            v = obj[i]
            _nested_obj_to_plain_dict(v, path + "[" + i + "]", result)
    else:
        raise Exception(f"TODO: type={t}")


def plain() -> dotdict:
    global _plain

    if _plain is None:
        _plain = dotdict()
        data = current()
        for k in data:
            _nested_obj_to_plain_dict(data[k], k, _plain)

    return _plain


# --------------------------------------------------
