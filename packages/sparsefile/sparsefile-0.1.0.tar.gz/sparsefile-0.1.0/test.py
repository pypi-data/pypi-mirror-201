"""
Testing this stupid module is actually pretty hard. You will need to arrange an OS and
filesystem that supports sparse file (or doesn't), and check this script.
"""

import argparse
from pathlib import Path
import tempfile

from sparsefile import ensure_sparse, _sparsifier


def main():
    ap = argparse.ArgumentParser("file sparsity tester")
    ap.add_argument(
        "path",
        type=Path,
        help="directory where to try to create and manipulate a sparse file",
    )
    ap.add_argument(
        "--keep", "-k", action="store_true", help="keep the stupid temporary file"
    )
    args = ap.parse_args()
    p = args.path
    if not p.is_dir():
        raise ValueError(f"{p!r} is not a directory")

    print("backend is", _sparsifier)

    with tempfile.NamedTemporaryFile(
        dir=p, prefix="sparsetest.", delete=not args.keep, suffix=".bin"
    ) as f:
        total_length = 2 ** 20
        start, end = 4095, total_length - 1023

        f.write(b"x" * total_length)
        ensure_sparse(f, start, end - start)
        if not f.tell() == total_length:
            raise AssertionError("file position should have stayed the same")
        f.seek(0)
        data = f.read(total_length)
        expected_value = (
            b"x" * start + b"\0" * (end - start) + b"x" * (total_length - end)
        )
        if data != expected_value:
            raise AssertionError("file contents not as expected")

    if args.keep:
        print(f.name)


if __name__ == "__main__":
    main()
