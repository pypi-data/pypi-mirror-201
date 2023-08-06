from __future__ import annotations

from typing import Callable, AnyStr, Any

from .datalogger_map import DataLoggerMap


class Tag(str):
    def __new__(cls, tag_name: str, *args_func: object, func: Callable = None, desc: str = None, default: object = None):
        """
        Define a Tag to be used for logging data.

        Args:
            tag_name: The name of the tag.
            args_func: Optional arguments to pass to func.
            func: An optional argument to define a function to call when a measurement using this tag is logged to the dataset.
             Using this argument will turn the tag into a tag that may be handled automatically by the datalogger.
            desc: An optional description of the tag.
            default: An optional argument for defining a default value so the value doesn't have to be logged manually.

        Raises:
            ValueError: If both func and default are not None.
        """
        if func and default:
            raise ValueError(f"Both 'func' and 'default' cannot be configured at the same time.")

        obj = super().__new__(cls, tag_name)
        obj.tag_name = tag_name
        obj.func = func
        obj.desc = desc
        obj.default = default
        if not args_func:
            args_func = tuple()
        obj.args_func = args_func
        return obj


class TagMap(DataLoggerMap):
    @property
    def key_type(self):
        return Tag

    def add(self, t: Tag, v: Any):
        assert t not in self, f"Tag {t} is already present in the tag-map (it is mapped to {self.get(t)})"
        self.update({t: v})

    def copy(self) -> TagMap[AnyStr, Any]:
        r = TagMap(super(TagMap, self).copy())
        return r
