"""v0.1.4c.

Revision ID: 2efe1dee9baf
Revises: e7151581f790
Create Date: 2023-01-30 15:03:43.834723

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2efe1dee9baf"
down_revision = "e7151581f790"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "account",
        sa.Column("avatar_url", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )


def downgrade() -> None:
    pass
