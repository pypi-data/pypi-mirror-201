"""
[![codecov](https://codecov.io/gh/cariad/checksome/branch/main/graph/badge.svg?token=I6zCxsU9be)](https://codecov.io/gh/cariad/checksome)

# Introduction

**Checksome** is a Python package and command line tool for generating and
comparing file checksums.

# Supported algorithms

Checksome can be extended to support any algorithm, and supports the following
natively:

| Algorithm | Command line value |
| -         | -                  |
| SHA256    | `sha256`           |

# Installation

Checksome requires Python 3.9 or later and can be installed from
[PyPI](https://pypi.org/project/checksome/).

```shell
pip install checksome
```

# Command line usage

Pass the file path and algorithm to `checksome` to get its checksum.

For example:

```console
$ checksome clowns.jpg sha256

b807b7c00e6052f2f5b23a4fc0716357e309cf6425a7ea93b766e7f127f64be0
```

# Python usage

## One-off checksums

To generate a single checksum for a file, call `checksum()` with the path and
type of algorithm to use.

If an offset is passed then the checksum will be calculated only for bytes from
that offset. If the offset is omitted then the file will be read from the start.

If a length is passed then the checksum will be calculated only for that given
length of bytes. If the length is omitted then the file will be read to the end.

```python
from checksome import checksum, SHA256

cs = checksum("clowns.jpg", SHA256)
# SHA256 checksum of "clowns.jpg"

cs = checksum("clowns.jpg", SHA256, offset=100, length=2000)
# SHA256 checksum of the 2,000 bytes following the 100th
# byte of "clowns.jpg"
```

To check if a file has a given checksum, call `has_checksum()`.

```python
from checksome import has_checksum, SHA256

has_checksum("clowns.jpg", SHA256, "b90...")
# True or False

has_checksum("clowns.jpg", SHA256, "b90...", offset=100, length=2000)
# True or False
```

The expected checksum can be passed as either bytes or a hexadecimal string.

`has_checksum()` isn't any more efficient than calling `checksum()` and
comparing the checksums yourself, but `has_checksum()` does provide some debug
logging that might be useful.

## Multiple checksums

If you need to generate multiple checksums for a file -- for example, to query
multiple byte ranges -- then creating a `ChecksumReader` is the most efficient
approach.

Rather than create a `ChecksumReader` directly, use the `checksum_reader`
context manager instead:

```python
from checksome import checksum_reader, SHA256

with checksum_reader("clowns.jpg", SHA256) as r:
    a = r.checksum(length=1024)
    # SHA256 checksum of the first 1,024 bytes

    b = r.checksum(offset=1024, length=1024)
    # SHA256 checksum of the second 1,024 bytes

    c = r.checksum(offset=2048)
    # SHA256 checksum of all remaining bytes
```

## Adding your own algorithm

To use a hashing algorithm that isn't supported natively by Checksome, implement
the `Algorithm` abstract class then pass that new class into any function that
requires an algorithm.

See the `SHA256` class for an example.

# Support

Please submit all your questions, feature requests and bug reports at
[github.com/cariad/checksome/issues](https://github.com/cariad/checksome/issues).
Thank you!

# Licence

Checksome is [open-source](https://github.com/cariad/checksome) and released
under the [MIT License](https://github.com/cariad/checksome/blob/main/LICENSE).

You don't have to give attribution in your project, but -- as a freelance
developer with rent to pay -- I appreciate it!

# Author

Hello! 👋 I'm **Cariad Eccleston**, and I'm a freelance Amazon Web Services
architect, DevOps evangelist, CI/CD pipeline engineer and backend developer.

You can find me at [cariad.earth](https://cariad.earth),
[github/cariad](https://github.com/cariad),
[linkedin/cariad](https://linkedin.com/in/cariad) and on Mastodon at
[@cariad@tech.lgbt](https://tech.lgbt/@cariad).
"""

from importlib.resources import open_text

from checksome.algorithms import SHA256, Algorithm
from checksome.checks import checksum, checksum_reader, has_checksum
from checksome.reader import ChecksumReader

with open_text(__package__, "VERSION") as t:
    __version__ = t.readline().strip()

__all__ = [
    "Algorithm",
    "ChecksumReader",
    "SHA256",
    "checksum",
    "checksum_reader",
    "has_checksum",
]
