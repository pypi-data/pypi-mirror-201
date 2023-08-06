import typing as tp
from collections.abc import Mapping, Sequence, Set
from dataclasses import is_dataclass

from playground.core.expcache.hashing import JSON_TYPE_CASTER
from playground.core.expcache.types_ import (
    Artifact,
    LazyObject,
    is_primitive_type,
    is_registered_custom_type,
    is_supported_obj_type,
)


def analyze_inputs(value: tp.Any) -> tp.List[tp.Tuple[tp.Union[str, int, tp.Type]]]:
    def _valid_obj(obj: tp.Any) -> bool:
        return (
            is_primitive_type(obj)
            or obj.__class__ in JSON_TYPE_CASTER
            or isinstance(obj, Set)
            or isinstance(value, LazyObject)
            or isinstance(value, Artifact)
            or is_dataclass(obj)
        )

    if _valid_obj(obj=value):
        return []

    invalid_object_type_paths = []
    if isinstance(value, Mapping):
        for key in value:
            if isinstance(value[key], (Mapping, Sequence)):
                paths = analyze_inputs(value=value[key])
                invalid_object_type_paths.extend([(key, *path) for path in paths])
            elif not _valid_obj(obj=value[key]):
                invalid_object_type_paths.append((key, value[key].__class__))
    elif isinstance(value, Sequence):
        for idx in range(len(value)):
            if isinstance(value[idx], (Mapping, Sequence)):
                paths = analyze_inputs(value=value[idx])
                invalid_object_type_paths.extend([(idx, *path) for path in paths])
            elif not _valid_obj(obj=value[idx]):
                invalid_object_type_paths.append((idx, value[idx].__class__))
    return invalid_object_type_paths  # type: ignore


def analyze_complex_types_in_object(
    value: tp.Any, only_artifacts: bool = False
) -> tp.List[tp.Tuple[tp.Union[str, int]]]:
    if (
        is_dataclass(value)
        or is_primitive_type(value)
        or isinstance(value, (Set, LazyObject))
        or is_registered_custom_type(value.__class__)
    ):
        return []
    complex_objects_path = []
    if isinstance(value, Mapping):
        for key in value:
            val = value[key]
            if (only_artifacts and isinstance(val, Artifact)) or (
                not only_artifacts
                and not (is_supported_obj_type(obj=val, include_custom=False) or isinstance(val, LazyObject))
            ):
                complex_objects_path.append((key,))
            else:
                paths = analyze_complex_types_in_object(value=val, only_artifacts=only_artifacts)
                complex_objects_path.extend([(key, *path) for path in paths])  # type: ignore
    elif isinstance(value, Sequence):
        for idx in range(len(value)):
            val = value[idx]
            if (only_artifacts and isinstance(val, Artifact)) or (
                not only_artifacts
                and not (is_supported_obj_type(obj=val, include_custom=False) or isinstance(val, LazyObject))
            ):
                complex_objects_path.append((idx,))
            else:
                paths = analyze_complex_types_in_object(value=value[idx], only_artifacts=only_artifacts)
                complex_objects_path.extend([(idx, *path) for path in paths])  # type: ignore
    return complex_objects_path


def analyze_lazy_objects(value: tp.Any) -> tp.List[str]:
    if is_primitive_type(value) or isinstance(value, Set) or is_dataclass(value):
        return []

    metadata_paths = []
    if isinstance(value, Mapping):
        for key in value:
            val = value[key]
            if isinstance(val, LazyObject):
                metadata_paths.append((key,))
            else:
                paths = analyze_lazy_objects(value=val)
                metadata_paths.extend([(key, *path) for path in paths])  # type: ignore
    elif isinstance(value, Sequence):
        for idx in range(len(value)):
            val = value[idx]
            if isinstance(val, LazyObject):
                metadata_paths.append((idx,))
            else:
                paths = analyze_lazy_objects(value=val)
                metadata_paths.extend([(idx, *path) for path in paths])  # type: ignore
    return metadata_paths  # type: ignore
