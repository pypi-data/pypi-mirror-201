"""v0.1.4d.

Revision ID: f2cb77148a6e
Revises: 2efe1dee9baf
Create Date: 2023-02-06 07:04:43.076136

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f2cb77148a6e"
down_revision = "2efe1dee9baf"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "account_instance",
        sa.Column("account_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("instance_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("permission", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["account.id"],
            name=op.f("fk_account_instance_account_id_account"),
        ),
        sa.PrimaryKeyConstraint(
            "account_id", "instance_id", name=op.f("pk_account_instance")
        ),
    )
    op.create_index(
        op.f("ix_account_instance_account_id"),
        "account_instance",
        ["account_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_account_instance_created_at"),
        "account_instance",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_account_instance_instance_id"),
        "account_instance",
        ["instance_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_account_instance_updated_at"),
        "account_instance",
        ["updated_at"],
        unique=False,
    )
    op.add_column(
        "instance",
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.add_column("instance", sa.Column("public", sa.Boolean(), nullable=True))
    op.execute(
        """
    INSERT INTO account_instance
    SELECT
        account_id,
        id as instance_id,
        'admin' as permission,
        created_at,
        created_at as updated_at
    FROM instance
    """
    )


def downgrade() -> None:
    pass
