import inspect
import os
from typing import Any, Callable, Dict, List, Optional, Set

from diskcache import Cache
from playground.core.expcache.hashing import function_source_hash, hash_arguments

if os.getenv("CACHE_PATH") is None:
    raise Exception("CACHE_PATH envronment variable is not set")

cachedb = Cache(os.getenv("CACHE_PATH"))


def remove_function_from_cache(f: Callable) -> None:
    source_codes: Set[str] = cachedb.get(f.__name__) or []  # type: ignore
    if inspect.getsource(f) in source_codes:
        source_codes.remove(inspect.getsource(f))
        cachedb.set(f.__name__, list(source_codes))
        if not source_codes:
            fnames = get_cached_function_names()
            fnames.remove(f.__name__)
            cachedb.set("function_names", fnames)

    f_hash = function_source_hash(f=f)
    cached_arguments: List[Dict[str, Any]] = cachedb.get(f_hash) if f_hash in cachedb else []
    for arguments in cached_arguments:
        a_hash = hash_arguments(arguments=arguments)
        full_hash = f_hash + a_hash
        cachedb.delete(full_hash)


def get_cached_function_source_code_by_name(fname: str) -> Optional[List[str]]:
    return cachedb.get(fname)  # type: ignore


def clear_cache() -> None:
    cachedb.clear()


def get_available_caches(f: Callable) -> List[Dict[str, Any]]:
    f_hash = function_source_hash(f=f)
    return cachedb.get(f_hash) if f_hash in cachedb else []  # type: ignore


def get_cached_function_names() -> List[str]:
    return cachedb.get("function_names") or []


def is_result_available(f: Callable, arguments: Dict[str, Any]) -> bool:
    f_hash = function_source_hash(f=f)
    a_hash = hash_arguments(arguments=arguments)
    full_hash = f_hash + a_hash
    return full_hash in cachedb


def maybe_register_new_function(f: Callable) -> None:
    functions_keys: Set[str] = set(cachedb.get("function_names") or [])
    if f.__name__ not in functions_keys:
        functions_keys.add(f.__name__)
        cachedb.set("function_names", list(functions_keys))


def maybe_register_new_source_code(f: Callable) -> None:
    available_source_codes: Set[str] = set(cachedb.get(f.__name__) or [])
    if inspect.getsource(f) not in available_source_codes:
        available_source_codes.add(inspect.getsource(f))
        cachedb.set(f.__name__, list(available_source_codes))


def save_function_call_result(f: Callable, arguments: Dict[str, Any], result: Any) -> None:
    maybe_register_new_function(f=f)
    maybe_register_new_source_code(f=f)

    f_hash = function_source_hash(f=f)
    a_hash = hash_arguments(arguments=arguments)
    full_hash = f_hash + a_hash
    cached_arguments: List[Dict[str, Any]] = cachedb.get(f_hash) if f_hash in cachedb else []
    if full_hash not in cachedb:
        cached_arguments.append(arguments)
        cachedb.set(f_hash, cached_arguments)
    cachedb.set(full_hash, result)


def get_function_call_result(f: Callable, arguments: Dict[str, Any]) -> Optional[Any]:
    f_hash = function_source_hash(f=f)
    a_hash = hash_arguments(arguments=arguments)
    full_hash = f_hash + a_hash
    return cachedb.get(full_hash)
