import typing as tp

from loguru import logger
from playground.core.expcache.analyzer import analyze_complex_types_in_object, analyze_lazy_objects
from playground.core.expcache.serde import _deserialize, _serialize
from playground.core.expcache.types_ import Artifact, LazyObject, is_collection, is_dataclass, is_primitive_type


def maybe_transform_output(output: tp.Any, output_dir: str) -> tp.Any:
    if isinstance(output, (LazyObject)) or is_primitive_type(output) or is_dataclass(output):
        return output
    elif isinstance(output, Artifact):
        logger.info(f"Serializing {output.obj.__class__} to {output_dir}")
        new_path = _serialize(output=output.obj, output_dir=output_dir)
        return LazyObject(path=new_path, _type=output.obj.__class__)
    elif not is_collection(output):
        raise ValueError(
            "Only primitives, dataclasses, collections or registered custom types are supported in the output, "
            "however there are custom types that should be registered first and specified as artifacts: "
            + str(output.__class__)
        )

    artifact_paths = analyze_complex_types_in_object(value=output, only_artifacts=True)
    additional_paths = analyze_complex_types_in_object(value=output)
    unspecified_complex_returns = set(additional_paths) - set(artifact_paths)
    if unspecified_complex_returns:
        output_str = ", ".join([f"{'.'.join(map(str, path))}" for path in unspecified_complex_returns])
        raise ValueError(
            "Only primitives, dataclasses, collections or registered custom types are supported in the output,"
            " however there are custom types that should be registered first and specified as artifacts: " + output_str
        )

    output_transformed = output
    if artifact_paths:
        for accessors in artifact_paths:
            object = output_transformed
            prev_obj = None
            for accessor in accessors:
                prev_obj = object
                object = object[accessor]
            if isinstance(object, Artifact):
                object = object.obj
            logger.info(f"Serializing {object.__class__} to {output_dir}")
            new_path = _serialize(output=object, output_dir=output_dir)
            prev_obj[accessor] = LazyObject(path=new_path, _type=object.__class__)  # type: ignore

    return output_transformed


def modify_lazy_objects(input: tp.Dict, cnt: int) -> tp.Any:
    lazy_object_paths = analyze_lazy_objects(value=input)
    if lazy_object_paths:
        for accessors in lazy_object_paths:
            object = input
            for accessor in accessors:
                object = object[accessor]
            lazy_object = tp.cast(LazyObject, object)
            lazy_object.expcache_ref_cnt += cnt
            if lazy_object.expcache_ref_cnt < 0:
                raise ValueError("expcache_ref_cnt is negative")
            if lazy_object.expcache_ref_cnt == 1 and lazy_object.data is None:
                logger.info(
                    f"Deserializing {lazy_object._type} with lazy object's key chain"
                    " '{'.'.join(map(str, accessors))}' from {lazy_object.path}"
                )
                lazy_object.data = _deserialize(lazy_object=lazy_object)
            elif lazy_object.expcache_ref_cnt == 0 and lazy_object.data is not None:
                lazy_object.data = None
