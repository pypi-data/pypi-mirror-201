import contextlib
import os
from pathlib import Path
import platform
import struct
from typing import IO, Union

from .exc import SparsifyError


_FALLOC_FL_KEEP_SIZE = 1
_FALLOC_FL_PUNCH_HOLE = 2
_F_PUNCHHOLE = 99


class Sparsifier:
    buffer_size = 65536

    def __init__(self):
        self.init()

    def init(self):
        pass

    def _validate_length_offset(self, offset, length):
        if offset < 0:
            raise ValueError("offset must be nonnegative")
        if length < 0:
            raise ValueError("length must be nonnegative")

    def ensure_zeros_maybe_sparse(
        self, path: Union[str, Path, int, IO], offset: int, length: int
    ):
        self._validate_length_offset(offset, length)
        with self._open(path) as f:
            # enlarge file to ensure it's at least offset+length bytes long
            old_size = self._ensure_minimum_file_size(file=f, size=offset + length)

            # attempt to poke hole
            success = self._maybe_sparse(file=f, offset=offset, length=length)

            # if attempt failed, fallback to writing zeros
            if not success:
                # even if `_maybe_sparse` failed, try not to write explicit zeros
                # to the otherwise potentially sparse region that was opened up
                # by `_ensure_minimum_file_size`
                a = min(old_size, offset)
                b = min(old_size, offset + length)
                self._write_zeros(file=f, offset=a, length=b - a)
            return success

    def ensure_sparse(self, path: Union[str, Path, int, IO], offset: int, length: int):
        self._validate_length_offset(offset, length)
        with self._open(path) as f:
            return self._ensure_sparse(file=f, offset=offset, length=length)

    def maybe_sparse(
        self, path: Union[str, Path, int, IO], offset: int, length: int
    ) -> bool:
        self._validate_length_offset(offset, length)
        with self._open(path) as f:
            return self._maybe_sparse(file=f, offset=offset, length=length)

    def ensure_minimum_file_size(
        self, path: Union[str, Path, int, IO], size: int
    ) -> int:
        with self._open(path) as f:
            return self._ensure_minimum_file_size(file=f, size=size)

    def _ensure_minimum_file_size(self, file: IO, size: int) -> int:
        old = file.tell()
        try:
            old_size = file.seek(0, os.SEEK_END)
            if old_size < size:
                file.seek(size - 1)
                file.write(b"\0")
            return old_size
        finally:
            file.seek(old)

    def _ensure_sparse(self, file: IO, offset: int, length: int):
        try:
            raise NotImplementedError("not supported on fallback backend")
        except NotImplementedError as exc:
            raise self._make_sparsify_error(file) from exc

    def _maybe_sparse(self, file: IO, offset: int, length: int) -> bool:
        try:
            self._ensure_sparse(file=file, offset=offset, length=length)
            return True
        except SparsifyError:
            return False

    def _open(self, path: Union[str, Path, int, IO]) -> IO:
        if hasattr(path, "fileno"):
            return contextlib.nullcontext(path)
        else:
            return open(path, "r+b")

    def _write_zeros(self, file: IO, offset, length):
        zeros = memoryview(bytes(self.buffer_size))

        old = file.tell()
        try:
            file.seek(offset)
            while length > 0:
                length -= file.write(zeros[:length])
        finally:
            file.seek(old)

    def _make_sparsify_error(self, file):
        return SparsifyError("failed to sparsify file", repr(file))


class LinuxSparsifier(Sparsifier):
    def init(self):
        if platform.system() != "Linux":
            raise NotImplementedError

        import ctypes
        from ctypes import util

        self._ctypes = ctypes
        self._ctypes_util = util
        self._linux_fallocate = self._get_linux_fallocate()

    def _get_ctypes_libc(self):
        libc_name = self._ctypes_util.find_library("c")
        libc = self._ctypes.CDLL(libc_name, use_errno=True)
        return libc

    def _get_linux_fallocate(self):
        ctypes = self._ctypes
        libc = self._get_ctypes_libc()

        c_off_t = ctypes.c_int64

        _fallocate = libc.fallocate
        _fallocate.restype = ctypes.c_int
        _fallocate.argtypes = [ctypes.c_int, ctypes.c_int, c_off_t, c_off_t]

        return _fallocate

    def _ensure_sparse(self, file: IO, offset: int, length: int):
        fd = file.fileno()
        mode = _FALLOC_FL_KEEP_SIZE | _FALLOC_FL_PUNCH_HOLE
        try:
            if self._linux_fallocate(fd, mode, offset, length) != 0:
                raise IOError(self._ctypes.get_errno(), "fallocate failed")
        except Exception as exc:
            raise self._make_sparsify_error(file) from exc


class WindowsSparsifier(Sparsifier):
    def init(self):
        if platform.system() != "Windows":
            raise NotImplementedError

        from . import windows

        self._module = windows

    def _ensure_sparse(self, file: IO, offset: int, length: int):
        try:
            self._module.windows_make_sparse(file=file, offset=offset, length=length)
        except Exception as exc:
            raise self._make_sparsify_error(file) from exc


class DarwinSparsifier(Sparsifier):  # Mac OS X
    def init(self):
        if platform.system() != "Darwin":
            raise NotImplementedError

        import fcntl

        self._fcntl = fcntl

    def _ensure_sparse(self, file: IO, offset: int, length: int):
        if length <= 0:
            return

        data = struct.pack("@IIQQ", 0, 0, offset, length)
        try:
            self._fcntl.fcntl(file.fileno(), _F_PUNCHHOLE, data)
        except Exception as exc:
            raise self._make_sparsify_error(file) from exc
