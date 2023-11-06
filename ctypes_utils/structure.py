from __future__ import annotations

import ctypes
import typing

from ctypes_utils.converter import to_pytype

if typing.TYPE_CHECKING:
    from collections.abc import Sequence
    from ctypes import _CData

_FieldsType: typing.TypeAlias = "Sequence[tuple[str, type[_CData]] | tuple[str, type[_CData], int]]"


def _repr(obj: typing.Any) -> str:
    if isinstance(obj, ctypes.Array):
        return f'[{", ".join(_repr(x) for x in obj)}]'
    if isinstance(obj, ctypes._Pointer):  # noqa: SLF001
        try:
            return repr(obj.contents)
        except ValueError:
            return repr(None)
    return repr(obj)


class StructureInitMixin:
    _fields_: typing.ClassVar[_FieldsType]

    def __init__(self, *args, **kwargs):
        argkeys = set(kwargs.keys())
        fields = {f for f, *_ in self._fields_}
        if argkeys - fields:
            msg = f"not expected argument(s): {argkeys - fields}"
            raise TypeError(msg)
        super().__init__(*args, **kwargs)


class StructureReprMixin:
    _fields_: typing.ClassVar[_FieldsType]

    def __repr__(self):
        args = ", ".join(f'{k}={_repr(getattr(self, k)) if self._show(k) else "..."}' for k, *_ in self._fields_)
        return f"{self.__class__.__name__}({args})"

    def _show(self, field: str) -> bool:  # noqa: ARG002
        """`field` を `__repr__` で表示するかどうか"""
        return True


class StructureTodictMixin:
    _fields_: typing.ClassVar[_FieldsType]

    def to_dict(self) -> dict[str, typing.Any]:
        return to_pytype(self)  # type: ignore


class Structure(
    StructureInitMixin,
    StructureReprMixin,
    StructureTodictMixin,
    ctypes.Structure,
):
    _fields_: typing.ClassVar[_FieldsType]
