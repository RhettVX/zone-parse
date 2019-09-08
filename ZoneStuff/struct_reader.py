from io import BufferedReader
from pathlib import Path
from struct import calcsize, unpack_from, Struct


class BinaryStructReader(BufferedReader):
    """
    A convenience wrapper for reading binary files.
    """
    path: Path

    _uint8 = Struct('B')

    # Big-endian structs
    _uint32BE = Struct('>I')
    _uint64BE = Struct('>Q')

    # Little-endian structs
    _uint32LE = Struct('<I')
    _uint64LE = Struct('<Q')
    _int32LE = Struct('<i')
    _float32LE = Struct('<f')

    def unpack_struct(self, fmt):
        size = calcsize(fmt)
        return unpack_from(fmt, self.read(size))

    def _read_struct(self, s: Struct):
        unpacked = s.unpack_from(self.read(s.size))
        if len(unpacked) == 1:
            return unpacked[0]
        else:
            return unpacked

    def uint8(self):
        return self._read_struct(self._uint8)

    def uint32LE(self):
        return self._read_struct(self._uint32LE)

    def uint32BE(self):
        return self._read_struct(self._uint32BE)

    def uint64LE(self):
        return self._read_struct(self._uint64LE)

    def uint64BE(self):
        return self._read_struct(self._uint64BE)

    def int32LE(self):
        return self._read_struct(self._int32LE)

    def float32LE(self, round_max=None):
        if round_max:
            return round(self._read_struct(self._float32LE), round_max)
        return self._read_struct(self._float32LE)

    def ztstring(self):
        return ''.join(iter(lambda: self.read(1).decode('utf-8'), '\x00'))

    def string(self, length, encoding='utf-8'):
        return self.unpack_struct(str(length) + 's')[0].decode(encoding)

    def __init__(self, path: Path):
        file_io = path.open('rb')
        super().__init__(file_io)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __getitem__(self, item):
        return self.unpack_struct(item)
