import os
from datetime import datetime
from typing import Optional  # noqa
from uuid import UUID, uuid4

from sqlalchemy.orm import registry
from sqlmodel import Field, MetaData, PrimaryKeyConstraint
from sqlmodel import SQLModel as SQLModelPlain
from sqlmodel import UniqueConstraint

from ._timestamps import CreatedAt, UpdatedAt

# the complexity here comes from avoiding collisions with
# lamindb schemas when other databases are set up
if "LN_SERVER_DEPLOY" not in os.environ:

    class SQLModel(SQLModelPlain, registry=registry()):  # type: ignore
        pass

else:  # and still being able to test migrations
    from sqlmodel import SQLModel  # type: ignore  # noqa


class User(SQLModel, table=True):  # type: ignore
    __tablename__ = "users"
    metadata = MetaData(schema="auth")
    id: Optional[UUID] = Field(primary_key=True)


class Account(SQLModel, table=True):  # type: ignore
    """Accounts."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: Optional[UUID] = Field(foreign_key=User.id, index=True)
    """Maybe None because it may be an organizational account."""
    lnid: str = Field(index=True, unique=True)
    """User-facing base62 ID."""
    handle: str = Field(index=True, unique=True)
    name: Optional[str] = Field(default=None, index=True)
    bio: Optional[str] = None
    website: Optional[str] = None
    github_handle: Optional[str] = None
    twitter_handle: Optional[str] = None
    linkedin_handle: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class Organization(SQLModel, table=True):  # type: ignore
    """User metadata."""

    id: Optional[UUID] = Field(primary_key=True, foreign_key=Account.id)


class Storage(SQLModel, table=True):  # type: ignore
    """Storage locations.

    A dobject or run-associated file can be stored in any desired S3,
    GCP, Azure or local storage location. This table tracks these locations
    along with metadata.
    """

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    account_id: UUID = Field(foreign_key=Account.id, index=True)
    """ID of owning account."""
    root: str = Field(index=True, unique=True)
    """An s3 path, a local path, etc."""  # noqa
    type: Optional[str] = None
    """Local vs. s3 vs. gcp etc."""
    region: Optional[str] = None
    """Cloud storage region if applicable."""
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class Instance(SQLModel, table=True):  # type: ignore
    """Instances."""

    __table_args__ = (UniqueConstraint("account_id", "name"),)
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    account_id: UUID = Field(foreign_key=Account.id, index=True)
    """ID of owning account."""
    name: str
    """Instance name."""
    storage_id: UUID = Field(foreign_key=Storage.id, index=True)
    """Default storage for loading an instance."""
    db: Optional[str] = Field(default=None, unique=True)
    """Database connection string. None for SQLite."""
    schema_str: Optional[str] = None
    """Comma-separated string of schema modules."""
    description: Optional[str] = None
    """Short text describing the instance."""
    public: Optional[bool] = False
    """Flag indicating if the instance is publicly visible."""
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class AccountInstance(SQLModel, table=True):  # type: ignore
    """Relationships between accounts and instances."""

    __tablename__ = "account_instance"
    __table_args__ = (PrimaryKeyConstraint("account_id", "instance_id"),)

    account_id: UUID = Field(foreign_key=Account.id, index=True)
    instance_id: UUID = Field(foreign_key=Instance.id, index=True)
    permission: str = "read-only"
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt
