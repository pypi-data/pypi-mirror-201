import copy
import dataclasses
import hashlib
import inspect
import json
import re
import typing as tp
from collections.abc import Mapping, Sequence, Set
from datetime import date, datetime

import numpy as np
from playground.core.expcache.types_ import LazyObject, is_primitive_type


def function_source_hash(f: tp.Callable) -> str:
    stripped_source_code = re.sub(r"(\s+|\n+)", "", inspect.getsource(f))
    return hashlib.sha256(stripped_source_code.encode()).hexdigest()


def hash_arguments(arguments: tp.Dict[str, tp.Any]) -> str:
    hashable_arguments = make_hashable(o=arguments)
    string_arguments = json.dumps(hashable_arguments)
    return hashlib.sha256(string_arguments.encode()).hexdigest()


def make_hashable(o: tp.Any, do_copy: bool = True) -> tp.Dict[tp.Any, tp.Any]:
    if is_primitive_type(o):
        return o  # type: ignore
    elif isinstance(o, Set):
        return tuple([make_hashable(e) for e in sorted(o)])  # type: ignore
    elif isinstance(o, Sequence):
        return tuple([make_hashable(e) for e in o])  # type: ignore
    elif isinstance(o, np.ndarray):
        if o.ndim > 1:
            return tuple([make_hashable(e) for e in o])  # type: ignore
        return tuple(o.tolist())  # type: ignore
    elif dataclasses.is_dataclass(o):
        return make_hashable(dataclasses.asdict(o), do_copy=False)  # type: ignore
    elif o.__class__ in JSON_TYPE_CASTER:
        return make_hashable(JSON_TYPE_CASTER[o.__class__](o))  # type: ignore
    elif not isinstance(o, Mapping):
        raise ValueError(
            f"String converter is not registered for an argument of class {o.__class__}."
            " Hash function will be unstable without it because of the default python behavior"
        )

    new_o = copy.deepcopy(o) if do_copy else o
    for k, v in new_o.items():
        new_o[k] = make_hashable(v)  # type: ignore

    return new_o  # type: ignore


JSON_TYPE_CASTER = {
    LazyObject: lambda lazy_object: repr(lazy_object),
    datetime: lambda x: str(x),
    date: lambda x: str(x),
}
