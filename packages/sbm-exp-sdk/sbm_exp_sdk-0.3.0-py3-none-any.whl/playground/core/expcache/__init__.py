import typing as tp
from functools import wraps
from pathlib import Path

from loguru import logger
from playground.core.expcache.analyzer import analyze_inputs
from playground.core.expcache.db import get_function_call_result, is_result_available, save_function_call_result
from playground.core.expcache.transformers import maybe_transform_output, modify_lazy_objects


def expcache(output_dir: str, track_func_code: tp.Optional[tp.Callable] = None) -> tp.Callable:
    if not output_dir.startswith("s3"):
        output_dir = str(Path(output_dir).expanduser().resolve())

    def wrapper(f: tp.Callable):
        func = track_func_code if track_func_code is not None else f

        @wraps(f)
        def wrapped(**kwargs) -> tp.Any:
            input_analysis = analyze_inputs(value=kwargs)
            if input_analysis:
                output_str = "\n\t".join([f"{'.'.join(map(str, path[:-1]))} -> {path[-1]}" for path in input_analysis])
                raise ValueError(
                    "Only dataclasses / Lazy objects / primitives / types"
                    " that have a registered caster to json serializable types"
                    " are supported as input types, but checker has found the following types during analysis:\n"
                    + output_str
                )

            if is_result_available(f=func, arguments=kwargs):
                logger.info(f"Cache hit for {f.__name__}")
                return get_function_call_result(f=func, arguments=kwargs)
            logger.info(f"Cache miss for {f.__name__}")
            modify_lazy_objects(input=kwargs, cnt=1)
            try:
                output = f(**kwargs)
            finally:
                modify_lazy_objects(input=kwargs, cnt=-1)
            output = maybe_transform_output(output=output, output_dir=output_dir)
            logger.info("Saving the result")
            save_function_call_result(f=func, arguments=kwargs, result=output)
            return output

        return wrapped

    return wrapper
