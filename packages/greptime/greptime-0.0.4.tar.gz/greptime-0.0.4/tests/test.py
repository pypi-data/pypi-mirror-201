from __future__ import annotations
from greptime import PyVector, coprocessor, i64

@coprocessor(args=["a", "b"])
def a()-> PyVector[i64]:
    return 0

print(a())