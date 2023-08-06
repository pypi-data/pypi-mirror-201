from ctypes import CDLL, c_char_p, c_uint32, c_void_p, py_object
from pathlib import Path

__all__ = ["YitiziMap"]

yitizi_lib = CDLL(str((Path(__file__).parent / "_lib.so").resolve()))

yitizi_lib.new_yitizi_map.restype = c_void_p
yitizi_lib.new_yitizi_map.argtypes = [c_char_p]

yitizi_lib.delete_yitizi_map.restype = None
yitizi_lib.delete_yitizi_map.argtypes = [c_void_p]

yitizi_lib.get_yitizi.restype = py_object
yitizi_lib.get_yitizi.argtypes = [c_void_p, c_uint32]


class YitiziMap:
    def __init__(
        self, path: str = str((Path(__file__).parent / "yitizi.tsv").resolve())
    ):
        self._ptr = yitizi_lib.new_yitizi_map(str(path).encode())

    def __del__(self):
        yitizi_lib.delete_yitizi_map(self._ptr)

    def _get(self, codepoint: int) -> list[int]:
        return yitizi_lib.get_yitizi(self._ptr, codepoint)

    def get(self, char: str) -> frozenset[str]:
        return frozenset(chr(codepoint) for codepoint in self._get(ord(char)))

    def __getitem__(self, char: str) -> frozenset[str]:
        return self.get(char)
