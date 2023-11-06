import ctypes
import ctypes.wintypes

import pytest

from ctypes_utils import to_pytype


@pytest.mark.parametrize(
    ("lhs", "rhs"),
    [
        (ctypes.c_bool(False), False),  # noqa: FBT003
        (ctypes.c_byte(0), 0),
        (ctypes.c_short(0), 0),
        (ctypes.c_int(0), 0),
        (ctypes.c_long(0), 0),
        (ctypes.c_longlong(0), 0),
        (ctypes.c_ubyte(0), 0),
        (ctypes.c_ushort(0), 0),
        (ctypes.c_uint(0), 0),
        (ctypes.c_ulong(0), 0),
        (ctypes.c_ulonglong(0), 0),
        (ctypes.c_size_t(0), 0),
        (ctypes.c_ssize_t(0), 0),
        (ctypes.c_float(0.0), 0.0),
        (ctypes.c_double(0.0), 0.0),
        (ctypes.c_longdouble(0.0), 0.0),
        (ctypes.c_char(b"A"), b"A"),
        (ctypes.c_char_p(b"spam"), b"spam"),
        (ctypes.c_wchar("A"), "A"),
        (ctypes.c_wchar_p("spam"), "spam"),
        (ctypes.c_void_p(), None),
        (ctypes.c_char_p(), None),
        (ctypes.c_wchar_p(), None),
    ],
)
def test_scalar(lhs, rhs):
    assert to_pytype(lhs) == rhs


def test_pointer():
    v = ctypes.c_int(57)
    p = ctypes.pointer(v)
    assert to_pytype(p)


def test_array():
    assert to_pytype((ctypes.c_int * 4)(0, 1, 2, 3)) == [0, 1, 2, 3]


def test_rect():
    class RECT(ctypes.Structure):
        _fields_ = [  # noqa: RUF012
            ("left", ctypes.wintypes.LONG),
            ("top", ctypes.wintypes.LONG),
            ("right", ctypes.wintypes.LONG),
            ("bottom", ctypes.wintypes.LONG),
        ]

    assert to_pytype(RECT(0, 1, 2, 3)) == {"left": 0, "top": 1, "right": 2, "bottom": 3}
    assert to_pytype(RECT(top=1)) == {"left": 0, "top": 1, "right": 0, "bottom": 0}


def test_nested():
    class Inner(ctypes.Structure):
        _fields_ = [  # noqa: RUF012
            ("a", ctypes.c_int),
            ("b", ctypes.c_bool),
        ]

    class Nested(ctypes.Structure):
        _fields_ = [  # noqa: RUF012
            ("inner", Inner),
            ("inner_array", Inner * 2),
        ]

    assert to_pytype(Nested()) == {
        "inner": {"a": 0, "b": False},
        "inner_array": [{"a": 0, "b": False}, {"a": 0, "b": False}],
    }
