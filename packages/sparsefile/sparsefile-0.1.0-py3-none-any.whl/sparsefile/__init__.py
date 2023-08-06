import logging
from pathlib import Path
from typing import IO, Union

from .exc import SparsifyError  # noqa
from .sparsifier import LinuxSparsifier, DarwinSparsifier, WindowsSparsifier, Sparsifier

logger = logging.getLogger(__name__)


def ensure_sparse(path: Union[str, Path, int, IO], offset: int, length: int) -> None:
    """
    Free the data blocks in file, decreasing filesystem usage. If the function
    fails to make the file sparse (due to lack of filesystem or OS support),
    :exc:`SparsifyError` will be raised.

    If ``offset + length`` lies beyond the end of the file, the file length may or
    may not increase.
    """
    return _sparsifier.ensure_sparse(path=path, offset=offset, length=length)


def maybe_sparse(path: Union[str, Path, int, IO], offset: int, length: int) -> bool:
    """
    Attempt to free the data blocks in file, decreasing filesystem usage. Return
    whether the attempt was successful.

    If ``offset + length`` lies beyond the end of the file, the file length may or
    may not increase.
    """
    return _sparsifier.maybe_sparse(path=path, offset=offset, length=length)


def ensure_zeros_maybe_sparse(
    path: Union[str, Path, int, IO], offset: int, length: int
) -> bool:
    """
    Attempt to free the data blocks in file, decreasing filesystem usage. Return
    whether the attempt was successful.

    Regardless of whether the attempt was successful, ensure that the file content
    bytes between ``offset`` and ``offset + length`` are zeroed out. The file will
    have a length at least ``offset + length``.
    """
    return _sparsifier.ensure_zeros_maybe_sparse(
        path=path, offset=offset, length=length
    )


def ensure_minimum_file_size(self, path: Union[str, Path, int, IO], size: int) -> int:
    """
    Ensure that the file is at least this large. Enlarge it in a sparse way if
    possible by writing a single zero byte at ``size - 1``.

    Return the file's previous size.
    """
    return _sparsifier.ensure_minimum_file_size(path, size)


def _autodetect_backend():
    for cls in (LinuxSparsifier, DarwinSparsifier, WindowsSparsifier, Sparsifier):
        try:
            return cls()
        except NotImplementedError:
            pass
        except Exception:
            logger.warning(
                "backend init failed", extra={"backend": str(cls)}, exc_info=True
            )


_sparsifier = _autodetect_backend()
