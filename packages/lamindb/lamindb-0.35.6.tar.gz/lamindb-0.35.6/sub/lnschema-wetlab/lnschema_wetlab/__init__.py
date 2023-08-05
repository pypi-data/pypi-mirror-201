"""Base classes for a wetlab schema (`vvhc`).

Import the package::

   import lnschema_wetlab

Base classes:

.. autosummary::
   :toctree: .

   ExperimentBase
   ExperimentTypeBase
   BiosampleBase
   TechsampleBase

Examples of derived classes, typically configured:

.. autosummary::
   :toctree: .

   Experiment
   ExperimentTypeBase
   BiosampleBase
   TechsampleBase

Development tools:

.. autosummary::
   :toctree: .

   dev
   link

"""
# This is lnschema-module vvhc.
_schema_id = "vvhc"
_name = "wetlab"
_migration = "bfda12fc80a8"
__version__ = "0.15rc2"

from . import dev, link
from ._core import (  # noqa
    Biosample,
    BiosampleBase,
    Experiment,
    ExperimentBase,
    ExperimentType,
    ExperimentTypeBase,
    Techsample,
    TechsampleBase,
)
