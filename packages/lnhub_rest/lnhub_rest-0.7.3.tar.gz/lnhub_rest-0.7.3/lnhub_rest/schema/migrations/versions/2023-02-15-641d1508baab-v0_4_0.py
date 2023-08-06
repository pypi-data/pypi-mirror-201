"""v0.4.0.

Revision ID: 641d1508baab
Revises: e7eef9775586
Create Date: 2023-02-15 16:51:40.852079

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "641d1508baab"
down_revision = "e7eef9775586"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "version_cbwk",
        sa.Column("v", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("migration", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("user_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["account.lnid"], name=op.f("fk_version_cbwk_user_id_account")
        ),
        sa.PrimaryKeyConstraint("v", name=op.f("pk_version_cbwk")),
    )
    op.create_index(
        op.f("ix_version_cbwk_created_at"), "version_cbwk", ["created_at"], unique=False
    )
    op.create_index(
        op.f("ix_version_cbwk_user_id"), "version_cbwk", ["user_id"], unique=False
    )


def downgrade() -> None:
    pass
