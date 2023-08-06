"""Schema."""
from .. import __version__ as _version

_schema_id = "cbwk"
_name = "hub"
_migration = "333fd693eac8"
__version__ = _version

from . import versions  # noqa
from ._core import Account, Instance, Organization, Storage, User  # noqa
