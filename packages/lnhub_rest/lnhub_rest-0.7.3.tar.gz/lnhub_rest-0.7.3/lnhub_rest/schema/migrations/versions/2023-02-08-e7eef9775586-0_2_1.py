"""0.2.1.

Revision ID: e7eef9775586
Revises: 9c02109e4faa
Create Date: 2023-02-08 14:45:04.261801

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e7eef9775586"
down_revision = "9c02109e4faa"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(op.f("uq_instance_db"), "instance", ["db"])


def downgrade() -> None:
    pass
