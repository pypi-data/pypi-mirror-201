import typing as tp

from loguru import logger
from playground.core.expcache.hashing import JSON_TYPE_CASTER
from playground.core.expcache.serde import DESERIALIZERS, SERIALIZERS
from playground.core.expcache.types_ import supported_custom_types


def register_custom_type(
    _type: tp.Type,
    serializer: tp.Callable[[tp.Any, str], str],
    deserializer: tp.Callable[[str], tp.Any],
) -> None:
    if _type in supported_custom_types:
        logger.info(f"{_type} is already registered, replacing serializer and deserializer")
    else:
        supported_custom_types.append(_type)
    SERIALIZERS[_type] = serializer  # type: ignore
    DESERIALIZERS[_type] = deserializer  # type: ignore


def register_json_type_caster(_type: tp.Type, type_caster: tp.Callable[[tp.Type], str]) -> None:
    JSON_TYPE_CASTER[_type] = type_caster
