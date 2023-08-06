import contextlib
import msvcrt
import struct
import win32file
import winioctlcon
from typing import IO


def windows_make_sparse(file: IO, offset: int, length: int) -> None:
    file.flush()

    def _reopen_if_possible():
        try:
            return open(file.name, "r+b")
        except PermissionError:
            return contextlib.nullcontext(file)

    # This is incredibly dumb but it seems it's unreliable to use the same file
    # descriptor to do FSCTL_SET_SPARSE and then immediately do
    # FSCTL_SET_ZERO_DATA. So we re-open the same file, do SET_SPARSE, then
    # close it and go on with FSCTL_SET_ZERO_DATA. But only if we can, depending
    # on whether the file was opened in exclusive mode.
    with _reopen_if_possible() as alt:
        h = msvcrt.get_osfhandle(alt.fileno())
        if length > 0:
            win32file.DeviceIoControl(h, winioctlcon.FSCTL_SET_SPARSE, None, None)

    h = msvcrt.get_osfhandle(file.fileno())
    end = offset + length
    offsets = struct.pack("@QQ", offset, end)
    win32file.DeviceIoControl(h, winioctlcon.FSCTL_SET_ZERO_DATA, offsets, None)
