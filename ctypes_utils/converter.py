from __future__ import annotations

import ctypes
from typing import Any, TypeVar, overload

_T = TypeVar("_T")


# fmt: off
@overload
def to_pytype(obj: ctypes.Structure) -> dict[str, Any]: ...

@overload
def to_pytype(obj: ctypes.Array[ctypes._SimpleCData[_T]]) -> list[_T]: ...

@overload
def to_pytype(obj: ctypes._Pointer[ctypes._SimpleCData[_T]]) -> _T | None: ...

@overload
def to_pytype(obj: ctypes._SimpleCData[_T]) -> _T: ...

@overload
def to_pytype(obj: ctypes.Array[Any]) -> list[Any]: ...

@overload
def to_pytype(obj: ctypes._Pointer[Any]) -> Any | None: ...

@overload
def to_pytype(obj: Any) -> Any: ...
# fmt: on


def to_pytype(obj: Any) -> Any:
    if isinstance(obj, ctypes.Structure):
        return {k: to_pytype(getattr(obj, k)) for k, _ in obj._fields_}  # noqa: SLF001
    if isinstance(obj, ctypes.Array):
        return [to_pytype(obj[i]) for i in range(obj._length_)]  # noqa: SLF001
    if isinstance(obj, ctypes._Pointer):  # noqa: SLF001
        try:
            return to_pytype(obj.contents)
        except ValueError:
            return None
    if isinstance(obj, ctypes._SimpleCData):  # noqa: SLF001
        return obj.value
    return obj
