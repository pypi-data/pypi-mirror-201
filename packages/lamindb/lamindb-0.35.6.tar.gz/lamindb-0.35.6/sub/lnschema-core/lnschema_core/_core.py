from datetime import datetime as datetime
from pathlib import Path
from typing import Any, List, Optional, Union, overload  # noqa

import anndata as ad
import pandas as pd
import sqlalchemy as sa
import sqlmodel
from cloudpathlib import CloudPath
from lamin_logger import logger
from pydantic.fields import PrivateAttr
from sqlmodel import Field, ForeignKeyConstraint, Relationship

from . import _name as schema_name
from ._link import FileFeatures, FolderFile, ProjectFolder, RunIn  # noqa
from ._timestamps import CreatedAt, UpdatedAt
from ._users import CreatedBy
from .dev import id as idg
from .dev._storage import filepath_from_file, filepath_from_folder
from .dev.sqlmodel import schema_sqlmodel
from .dev.type import TransformType

SQLModel, prefix, schema_arg = schema_sqlmodel(schema_name)


class User(SQLModel, table=True):  # type: ignore
    """User accounts.

    All data in this table is synched from the cloud user account to ensure a
    globally unique user identity.
    """

    id: str = Field(primary_key=True)
    email: str = Field(index=True, unique=True)
    """Primary user email used for logging in."""
    handle: str = Field(nullable=False, index=True, unique=True)
    """User handle."""
    name: Optional[str] = Field(index=True)
    """Long display name."""
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class Storage(SQLModel, table=True):  # type: ignore
    """Storage locations.

    A file or run-associated file can be stored in any desired S3,
    GCP, Azure or local storage location. This table tracks these locations
    along with metadata.
    """

    id: str = Field(default_factory=idg.storage, primary_key=True)
    root: str = Field(index=True)
    """Semantic identifier to the root of the storage location, like an s3 path, a local path, etc."""  # noqa
    type: Optional[str] = None
    """Local vs. s3 vs. gcp etc."""
    region: Optional[str] = None
    """Cloud storage region if applicable."""
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class Project(SQLModel, table=True):  # type: ignore
    """Projects."""

    id: str = Field(default_factory=idg.project, primary_key=True)
    name: str = Field(index=True)
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class Transform(SQLModel, table=True):  # type: ignore
    """Data transformations.

    Jupyter notebooks, pipelines, and apps.

    A pipeline is typically versioned software that can perform a data
    transformation/processing workflow. This can be anything from typical
    workflow tools (Nextflow, Snakemake, Prefect, Apache Airflow, etc.) to
    simple (versioned) scripts.

    Data can also be ingested & transformed through an app.
    """

    id: str = Field(default_factory=idg.pipeline, primary_key=True)
    v: str = Field(default="1", primary_key=True)
    """Version identifier, defaults to `"1"`.

    Use this to label different versions of the same transform.

    Consider using `semantic versioning <https://semver.org>`__
    with `Python versioning <https://peps.python.org/pep-0440/>`__.
    """
    name: str = Field(index=True)
    """A name for the transform, a pipeline name, or a file name of a notebook or script.
    """
    type: TransformType = Field(index=True, default=TransformType.pipeline)
    """The transform type.
    """
    title: Optional[str] = Field(index=True)
    """An additional title, like a notebook title.
    """
    reference: Optional[str] = Field(index=True)
    """Reference for the transform, e.g., a URL.
    """
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class Run(SQLModel, table=True):  # type: ignore
    """Runs of data transforms.

    A `run` is any transform of a `file`.

    Args:
        id: Optional[str] = None
        name: Optional[str] = None
        load_latest: bool = False - Load latest run for given notebook or pipeline.
        transform: Optional[Transform] = None
        inputs: List[File] = None
        outputs: List[File] = None

    It typically has inputs and outputs:

    - References to outputs are stored in the `file` table in the
      `source_id` column as a foreign key the `run`
      table. This is possible as every given `file` has a unique data source:
      the `run` that produced the `file`. However, note that a given
      `run` may output several `files`.
    - References to inputs are stored in the `run_in` table, a
      many-to-many link table between the `file` and `run` tables. Any
      `file` might serve as an input for many `runs`. Similarly, any
      `run` might have many `files` as inputs.
    """

    __table_args__ = (
        ForeignKeyConstraint(
            ["transform_id", "transform_v"],
            ["core.transform.id", "core.transform.v"],
        ),
        {"schema": schema_arg},
    )
    id: Optional[str] = Field(default_factory=idg.run, primary_key=True)
    name: Optional[str] = Field(default=None, index=True)
    external_id: Optional[str] = Field(default=None, index=True)
    transform_id: Optional[str] = Field(default=None, index=True)
    transform_v: Optional[str] = Field(default=None, index=True)
    transform: Transform = Relationship()
    outputs: List["File"] = Relationship(back_populates="source")
    inputs: List["File"] = Relationship(back_populates="targets", sa_relationship_kwargs=dict(secondary=RunIn.__table__))
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt

    _ln_identity_key: Optional[str] = PrivateAttr(default=None)
    # simulate query result

    def __init__(  # type: ignore
        self,
        *,
        id: Optional[str] = None,
        name: Optional[str] = None,
        load_latest: bool = False,
        external_id: Optional[str] = None,
        transform: Optional[Transform] = None,
        inputs: List["File"] = None,
        outputs: List["File"] = None,
    ):
        kwargs = {k: v for k, v in locals().items() if v and k != "self"}

        import lamindb as ln

        global_context = False
        if transform is None:
            if ln.context.transform is not None:
                global_context = True
                transform = ln.context.transform
            else:
                raise ValueError("Either call `ln.Run(transform=transform)` or `ln.track(transform=...)`.")

        if not isinstance(transform, Transform):
            raise TypeError("transform needs to be of type Transform")

        run = None
        if load_latest:
            run = ln.select(ln.Run, transform_id=transform.id, transform_v=transform.v).order_by(ln.Run.created_at.desc()).first()
            if run is not None:
                logger.info(f"Loaded run: {run}")
        elif id is not None:
            run = ln.select(ln.Run, id=id).one_or_none()
            if run is None:
                raise NotImplementedError("You can currently only pass existing ids")

        if run is None:
            kwargs.update(dict(transform_id=transform.id, transform_v=transform.v))
            super().__init__(**kwargs)
            self._ln_identity_key = None
        else:
            super().__init__(**run.dict())
            self._ln_identity_key = run.id  # simulate query result

        if global_context:
            if run is None:
                added_self = ln.add(self)
                self._ln_identity_key = added_self.id
                logger.info(f"Added run: {self}")
            ln.context.run = self


class Features(SQLModel, table=True):  # type: ignore
    """Feature sets.

    A feature set is represented by the hash of the set of primary keys and the feature type.

    The current supported feature types are lnschema_bionty.Gene,
    lnschema_bionty.Protein & lnschema_bionty.CellMarker.

    Guides:

    - :doc:`/guide/scrna`
    - :doc:`guide/flow`

    Examples:

    >>> import lnschema_bionty as bt
    >>> reference = bt.Gene(species="mouse")
    >>> features = ln.Features(adata, reference=reference)
    >>> file = ln.File(adata, name="Mouse Lymph Node scRNA-seq", features=features)

    Args:
        data: [Path, str, pd.DataFrame, ad.AnnData] - DataFrame or AnnData to parse.
        reference: Any = None - Reference for mapping features.
        id: str = None - Primary key.
        type: Any = None - Type of reference.
        files: List[File] - Files to link against.
    """

    id: str = Field(primary_key=True)  # use a hash
    type: str  # was called entity_type
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    files: List["File"] = Relationship(
        back_populates="features",
        sa_relationship_kwargs=dict(secondary=FileFeatures.__table__),
    )

    @overload
    def __init__(
        self,
        data: Union[Path, str, pd.DataFrame, ad.AnnData] = None,
        reference: Any = None,
    ):
        """Initialize from data."""
        ...

    @overload
    def __init__(
        self,
        id: Optional[str] = None,
        type: Optional[str] = None,
        files: List["File"] = [],
    ):
        """Initialize from fields."""
        ...

    def __init__(  # type: ignore
        self,
        data: Union[Path, str, pd.DataFrame, ad.AnnData] = None,
        reference: Any = None,
        *,
        id: str = None,
        type: Any = None,
        # continue with fields
        files: List["File"] = [],
    ):
        kwargs = {k: v for k, v in locals().items() if v and k != "self"}
        super().__init__(**kwargs)

    def __new__(
        cls,
        data: Union[Path, str, pd.DataFrame, ad.AnnData] = None,
        reference: Any = None,
        *,
        id: str = None,
        type: Any = None,
        # continue with fields
        files: List["File"] = [],
    ):
        if data is not None:
            from lamindb._file import get_features_from_data

            features = get_features_from_data(
                data=data,
                reference=reference,
            )
        else:
            features = super().__new__(cls)
        return features


class Folder(SQLModel, table=True):  # type: ignore
    """Data folders, collections of data objects.

    In LaminDB, a data folder is a collection of data objects (`File`).
    """

    id: str = Field(default_factory=idg.folder, primary_key=True)
    name: str = Field(index=True)
    files: List["File"] = Relationship(  # type: ignore  # noqa
        back_populates="folders",
        sa_relationship_kwargs=dict(secondary=FolderFile.__table__),
    )
    """:class:`~lamindb.File`."""
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt

    # private attributes are needed here to prevent sqlalchemy error
    _local_filepath: Optional[Path] = PrivateAttr()
    _cloud_filepath: Optional[CloudPath] = PrivateAttr()

    def path(self) -> Union[Path, CloudPath]:
        """Path on storage."""
        return filepath_from_folder(self)

    def tree(
        self,
        level: int = -1,
        limit_to_directories: bool = False,
        length_limit: int = 1000,
    ) -> None:
        """Print a visual tree structure."""
        from lamindb._folder import tree

        return tree(
            dir_path=self.path(),
            level=level,
            limit_to_directories=limit_to_directories,
            length_limit=length_limit,
        )

    def get(self, relpath: Union[str, Path, List[Union[str, Path]]], **fields):
        """Get files via relative path to folder."""
        from lamindb._folder import get_file

        return get_file(folder=self, relpath=relpath, **fields)

    @overload
    def __init__(
        self,
        folder: Union[Path, str] = None,
        *,
        name: Optional[str] = None,
    ):
        """Initialize from folder."""
        ...

    @overload
    def __init__(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
        files: List["File"] = [],
    ):
        """Initialize from fields."""
        ...

    def __init__(  # type: ignore
        self,
        folder: Union[Path, str] = None,
        *,
        # continue with fields
        id: Optional[str] = None,
        name: Optional[str] = None,
        x: List["File"] = [],
    ):
        if folder is not None:
            from lamindb._folder import get_folder_kwargs_from_data

            kwargs, privates = get_folder_kwargs_from_data(
                folder=folder,
                name=name,
            )
            if id is not None:
                kwargs["id"] = id
        else:
            kwargs = {k: v for k, v in locals().items() if v and k != "self"}

        super().__init__(**kwargs)
        if folder is not None:
            self._local_filepath = privates["_local_filepath"]
            self._cloud_filepath = privates["_cloud_filepath"]


Folder._objectkey = sa.Column("_objectkey", sqlmodel.sql.sqltypes.AutoString(), index=True)


class File(SQLModel, table=True):  # type: ignore
    """See lamindb for docstring."""

    id: str = Field(default_factory=idg.file, primary_key=True)
    name: Optional[str] = Field(index=True)
    suffix: Optional[str] = Field(default=None, index=True)
    """Suffix to construct the storage key. Defaults to `None`.

    This is a file extension if the `file` is stored in a file format.
    It's `None` if the storage format doesn't have a canonical extension.
    """

    size: Optional[int] = Field(default=None, sa_column=sa.Column(sa.BigInteger(), index=True))
    """Size in bytes.

    Examples: 1KB is 1e3 bytes, 1MB is 1e6, 1GB is 1e9, 1TB is 1e12 etc.
    """
    hash: Optional[str] = Field(default=None, index=True)
    """Hash (md5)."""

    # We need the fully module-qualified path below, as there might be more
    # schema modules with an ORM called "Run"
    source: Run = Relationship(back_populates="outputs")  # type: ignore
    """:class:`~lamindb.Run` that generated the `file`."""
    source_id: str = Field(foreign_key="core.run.id", index=True)
    """Source run id."""
    storage_id: str = Field(foreign_key="core.storage.id", index=True)
    """Storage root id."""
    features: List[Features] = Relationship(
        back_populates="files",
        sa_relationship_kwargs=dict(secondary=FileFeatures.__table__),
    )
    """Feature sets indexing this file."""
    folders: List[Folder] = Relationship(
        back_populates="files",
        sa_relationship_kwargs=dict(secondary=FolderFile.__table__),
    )
    """Folders that contain this file."""
    targets: List[Run] = Relationship(  # type: ignore
        back_populates="inputs",
        sa_relationship_kwargs=dict(secondary=RunIn.__table__),
    )
    """Runs that use this file as input."""
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt

    # private attributes are needed here to prevent sqlalchemy error
    _local_filepath: Optional[Path] = PrivateAttr()
    _cloud_filepath: Optional[CloudPath] = PrivateAttr()
    _clear_storagekey: Optional[str] = PrivateAttr()
    _memory_rep: Any = PrivateAttr()

    def path(self) -> Union[Path, CloudPath]:
        """Path on storage."""
        return filepath_from_file(self)

    def replace(self, data: Union[Path, str, pd.DataFrame, ad.AnnData], source: Optional[Run] = None, format: Optional[str] = None):
        """Replace data object."""
        from lamindb._file import get_file_kwargs_from_data

        if isinstance(data, (Path, str)):
            name_to_pass = None
        else:
            name_to_pass = self.name

        kwargs, privates = get_file_kwargs_from_data(
            data=data,
            name=name_to_pass,
            source=source,
            format=format,
        )

        if kwargs["name"] != name_to_pass:
            logger.warning("Your new filename does not match the previous filename. If you want to update in the DB, update it manually!")

        # we don't delete storage objects added through _objectkey
        if self._objectkey is None and self.suffix != kwargs["suffix"]:
            self._clear_storagekey = f"{self.id}{self.suffix}"

        self.size = kwargs["size"]
        self.hash = kwargs["hash"]
        self.suffix = kwargs["suffix"]
        self.source = kwargs["source"]
        self._local_filepath = privates["_local_filepath"]
        self._cloud_filepath = privates["_cloud_filepath"]
        self._memory_rep = privates["_memory_rep"]

        # new _objectkey will be written in ln.add
        sa.orm.attributes.set_attribute(self, "_objectkey", None)

    def stage(self, is_run_input: bool = False):
        """Download from storage if newer than in the cache.

        Returns a path to a locally cached on-disk object (say, a
        `.jpg` file).
        """
        from lamindb._load import stage as lnstage

        return lnstage(file=self, is_run_input=is_run_input)

    def load(self, stream: bool = False, is_run_input: bool = False):
        """Load from storage (stage on local disk or load to memory).

        Returns in-memory representation if configured (say, an `AnnData` object
        for an `h5ad` file).

        Otherwise, returns a path to a locally cached on-disk object (say, a
        `.jpg` file).
        """
        from lamindb._load import load as lnload

        return lnload(file=self, stream=stream, is_run_input=is_run_input)

    @overload
    def __init__(
        self,
        data: Union[Path, str, pd.DataFrame, ad.AnnData] = None,
        *,
        name: Optional[str] = None,
        features: List[Features] = [],
        source: Optional[Run] = None,
        id: Optional[str] = None,
        format: Optional[str] = None,
    ):
        """Initialize from data."""
        ...

    @overload
    def __init__(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
        source: Optional[Run] = None,
        suffix: Optional[str] = None,
        size: Optional[int] = None,
        hash: Optional[str] = None,
        source_id: Optional[str] = None,
        storage_id: Optional[str] = None,
        features: List[Features] = [],
        targets: List[Run] = [],
    ):
        """Initialize from fields."""
        ...

    def __init__(  # type: ignore
        self,
        data: Union[Path, str, pd.DataFrame, ad.AnnData] = None,
        *,
        features: List[Features] = None,
        source: Optional[Run] = None,
        format: Optional[str] = None,
        # continue with fields
        id: Optional[str] = None,
        name: Optional[str] = None,
        suffix: Optional[str] = None,
        size: Optional[int] = None,
        hash: Optional[str] = None,
        source_id: Optional[str] = None,
        storage_id: Optional[str] = None,
        targets: List[Run] = None,
    ):
        if features is None:
            features = []
        if targets is None:
            targets = []
        if not isinstance(features, List):
            features = [features]

        if data is not None:
            from lamindb._file import get_file_kwargs_from_data

            kwargs, privates = get_file_kwargs_from_data(
                data=data,
                name=name,
                source=source,
                format=format,
            )
            if id is not None:
                kwargs["id"] = id
            if features is not None:
                kwargs["features"] = features
        else:
            kwargs = {k: v for k, v in locals().items() if v and k != "self"}

        super().__init__(**kwargs)
        if data is not None:
            self._local_filepath = privates["_local_filepath"]
            self._cloud_filepath = privates["_cloud_filepath"]
            self._memory_rep = privates["_memory_rep"]


File._objectkey = sa.Column("_objectkey", sqlmodel.sql.sqltypes.AutoString(), index=True)
File.__table__.append_constraint(sa.UniqueConstraint("storage_id", "_objectkey", "suffix", name="uq_storage__objectkey_suffix"))
