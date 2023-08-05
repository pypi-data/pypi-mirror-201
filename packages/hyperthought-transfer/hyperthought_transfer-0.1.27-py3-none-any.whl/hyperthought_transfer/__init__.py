import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`  # noqa: E501
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover  # noqa: E501
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover  # noqa: E501

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "hyperthought-transfer"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from . import antivirus, manifest  # noqa: F401
