"""v0.1.4e.

Revision ID: 95073282294e
Revises: f2cb77148a6e
Create Date: 2023-02-06 07:37:46.234267

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "95073282294e"
down_revision = "f2cb77148a6e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "account_instance", "permission", existing_type=sa.VARCHAR(), nullable=False
    )
    op.execute(
        """
    UPDATE instance
    SET public = false
    """
    )
    op.alter_column("instance", "public", existing_type=sa.BOOLEAN(), nullable=False)


def downgrade() -> None:
    pass
