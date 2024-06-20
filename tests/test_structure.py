import ctypes
import typing

import pytest

from ctypes_utils import Structure


def test_structure():
    class C(Structure):
        _fields_: typing.ClassVar = [
            ("a", ctypes.c_int),
        ]

    c = C(a=42)

    assert repr(c) == "C(a=42)"
    assert c.to_dict() == {"a": 42}


def test_from_dict():
    class C(Structure):
        _fields_: typing.ClassVar = [
            ("a", ctypes.c_int),
        ]

    c = C.from_dict({"a": 42})

    assert repr(c) == "C(a=42)"
    assert c.to_dict() == {"a": 42}


def test_complex():
    class A(Structure):
        _fields_: typing.ClassVar = [
            ("a", ctypes.c_int),
        ]

    class B(Structure):
        _fields_: typing.ClassVar = [
            ("b", ctypes.c_int),
        ]

    class C(Structure):
        _fields_: typing.ClassVar = [
            ("a", A),
            ("b", B * 2),
            ("c", ctypes.c_int),
            ("ptr", ctypes.POINTER(ctypes.c_int)),
        ]

    c = C()
    assert repr(c) == "C(a=A(a=0), b=[B(b=0), B(b=0)], c=0, ptr=None)"
    assert c.to_dict() == {
        "a": {"a": 0},
        "b": [{"b": 0}, {"b": 0}],
        "c": 0,
        "ptr": None,
    }


def test_repr_show():
    class C(Structure):
        _fields_: typing.ClassVar = [
            ("a", ctypes.c_int),
            ("hidden", ctypes.c_int),
        ]

        def _show(self, field: str) -> bool:
            return field not in {"hidden"}

    c = C(a=42, hidden=57)
    assert repr(c) == "C(a=42, hidden=...)"
    assert c.to_dict() == {"a": 42, "hidden": 57}


def test_init_fails():
    class C(Structure):
        _fields_: typing.ClassVar = [
            ("a", ctypes.c_int),
        ]

    with pytest.raises(TypeError, match=r"not expected argument\(s\): .*"):
        C(b=1)

    with pytest.raises(TypeError, match=r"duplicate values for field .*"):
        C(1, a=1)

    with pytest.raises(TypeError, match=r"too many initializers"):
        C(1, 2)
