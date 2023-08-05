"""LaminDB: Manage R&D data & analyses.

Import the package::

   import lamindb as ln

The central class of the API is `File`, a wrapper for files, on-disk (`zarr`, etc.)
and in-memory data objects (`DataFrame`, `AnnData`, etc.).

.. autosummary::
   :toctree: .

   File
   Folder

Track runs of data transformations:

.. autosummary::
   :toctree: .

   Run
   Transform

Tracking data by features:

.. autosummary::
   :toctree: .

   Features

Query & manipulate data:

.. autosummary::
   :toctree: .

   select
   add
   delete

Manipulate data with open session:

.. autosummary::
   :toctree: .

   Session

Utility functions:

.. autosummary::
   :toctree: .

   track
   view

Basic entities:

.. autosummary::
   :toctree: .

   User
   Project
   StorageRoot

Schema - entities and their relations:

.. autosummary::
   :toctree: .

   schema

Setup:

.. autosummary::
   :toctree: .

   setup

Developer API:

.. autosummary::
   :toctree: .

   context
   settings
   dev
"""

__version__ = "0.35.6"  # denote a release candidate for 0.1.0 with 0.1rc1

# prints warning of python versions
from lamin_logger import logger as _logger
from lamin_logger import py_version_warning as _py_version_warning

_py_version_warning("3.8", "3.10")

from lndb import settings as _setup_settings
from lndb._migrate import check_deploy_migration as _check_migrate
from lndb.dev._settings_store import (
    current_instance_settings_file as _current_settings_file,
)

from . import _check_versions  # executes checks during import

_instance_setup = False
if (
    not _current_settings_file().exists()
    or _setup_settings.instance.storage.root is None
):
    _logger.warning(
        "You haven't yet setup an instance using the CLI. Please call"
        " `lamindb.setup.init()` or `lamindb.setup.load()`."
    )
else:
    try:
        _check_migrate(
            usettings=_setup_settings.user, isettings=_setup_settings.instance
        )
        _instance_setup = True
    except Exception:
        _logger.warning(
            "Your current instance cannot be reached, init or load a connectable"
            " instance."
        )

from lndb_storage import subset
from lndb_storage.object import lazy
from lnschema_core import Features, File, Folder, Project, Run  # noqa
from lnschema_core import Storage as StorageRoot
from lnschema_core import Transform, User  # noqa

from . import _amend_doc_strings  # noqa
from . import dev  # noqa
from . import schema  # noqa
from . import setup  # noqa
from ._context import context  # noqa

track = context._track  # noqa
from ._delete import delete  # noqa
from ._nb import nb  # noqa
from ._settings import settings
from ._view import view  # noqa
from .dev.db import Session  # noqa
from .dev.db._add import add  # noqa
from .dev.db._select import select  # noqa
