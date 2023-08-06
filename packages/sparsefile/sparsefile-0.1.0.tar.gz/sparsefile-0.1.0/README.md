# sparsefile

This module implements [sparse file](https://en.wikipedia.org/wiki/Sparse_file)
"hole punching" on GNU+Linux, Microsoft Windows, and probably Mac OS X (untested).
This allows you to quickly create sparse file gaps such that the gaps appear to be
filled with null (`b"\0"`) bytes but they don't occupy any actual disk space.

This is a pure-Python module which uses `ctypes`/`pywin32`/`fcntl` to do its dirty work.

# Dependencies

`pywin32` on Windows. None otherwise.

# Examples

First import the library and choose an appropriate victim.

```python
>>> from pathlib import Path
>>> import sparsefile
>>> path = Path("my_file.bin")
```

Then sparsification comes in three different flavours:

- `sparsefile.ensure_sparse(path, offset=1000, length=3000)`

  Make the byte range 1000-3999 (inclusive) sparse. If the OS or filesystem do
  not support the operation, raise a `SparsifyError`.

- `sparsefile.ensure_zeros_maybe_sparse(path, offset=1000, length=3000)`

  Fill the byte range 1000-3999 (inclusive) with zeros. The byte range will
  also be sparse _if_ the OS and filesystem support it. The function returns
  a boolean that indicates whether the byte range was successfully made sparse.

- `sparsefile.maybe_sparse(path, offset=1000, length=3000)`

  _Try_ to make the byte range 1000-3999 (inclusive) sparse. Do nothing if
  the OS or filesystem do not support it. If the file is currently shorter
  than 4000 bytes, then it will remain so.

# Issues

- The test suite is severely lacking.
- Hasn't been tested on OS X (sorry).
