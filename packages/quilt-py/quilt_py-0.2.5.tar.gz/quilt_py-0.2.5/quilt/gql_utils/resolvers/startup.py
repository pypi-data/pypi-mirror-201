import typing as T
import inspect
import time
from quilt import logs
from . import logic, helpers, models
from ..strawberry_utils import StrawMixin

logger = logs.create_logger(__name__)

PreloadRaw = models.PreloadRaw


RAW_PRELOADS_KEY = "raw_preloads"
PRELOADS_KEY = "preloads"


def merge_raw_preloads(
    field_name: str, raw_preload_lst: list[PreloadRaw]
) -> list[PreloadRaw]:
    if len(raw_preload_lst) <= 1:
        return raw_preload_lst
    merged_raw_pres = []
    fields_to_include_set: set[str] = set()
    for raw_pre in raw_preload_lst:
        if raw_pre.only_fields_to_include() and raw_pre.fields_to_include:
            fields_to_include_set.update(raw_pre.fields_to_include)
        else:
            merged_raw_pres.append(raw_pre)
    if merged_raw_pres:
        for i in merged_raw_pres:
            if not i.fields_to_include:
                i.fields_to_include = fields_to_include_set
            else:
                i.fields_to_include.update(fields_to_include_set)
    else:
        merged_raw_pres = [
            PreloadRaw(field_name=field_name, fields_to_include=fields_to_include_set)
        ]
    return merged_raw_pres


def create_preloads() -> None:
    start = time.time()
    for cls in StrawMixin.__subclasses__():
        for field in cls._type_definition.fields:
            straw_field = getattr(cls, field.name, None)
            if straw_field:
                d = straw_field.__dict__
                actual_return_type = helpers.return_type_from_return_annotation(
                    raw_return_type=straw_field.__annotations__["return"],
                    current_straw_type=cls,
                )
                if (
                    inspect.isclass(actual_return_type)
                    and issubclass(actual_return_type, StrawMixin)
                    and RAW_PRELOADS_KEY not in d
                ):
                    # if not in resolver, do not do this
                    if field.name in cls.Config.resolver_type._edge_resolver_map:
                        d[RAW_PRELOADS_KEY] = [
                            PreloadRaw(field_name=field.name, alias=field.name)
                        ]
                if raw_preloads := d.get(RAW_PRELOADS_KEY):
                    raw_preloads = T.cast(list[PreloadRaw], raw_preloads)
                    if PRELOADS_KEY not in d:
                        d[PRELOADS_KEY] = []

                    merged_raw_preloads = raw_preloads
                    if len(raw_preloads) > 1:
                        merged_raw_preloads = merge_raw_preloads(
                            field_name=field.name, raw_preload_lst=raw_preloads
                        )

                    for raw_preload in merged_raw_preloads:
                        # if not return_type given, get current return type
                        preload = logic.preload_raw_to_preload(
                            current_straw_type=cls,
                            preload_raw=raw_preload,
                            actual_return_type=actual_return_type,
                        )
                        d[PRELOADS_KEY].append(preload)
    took = time.time() - start
    logger.debug(f"preloaded done, took {round(took * 1000)} ms")
