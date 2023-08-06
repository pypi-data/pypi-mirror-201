"""v0.2.0.

Revision ID: 9c02109e4faa
Revises: 95073282294e
Create Date: 2023-02-06 15:54:02.292777

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9c02109e4faa"
down_revision = "95073282294e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key(
        op.f("fk_account_instance_instance_id_instance"),
        "account_instance",
        "instance",
        ["instance_id"],
        ["id"],
    )
    op.alter_column("instance", "public", existing_type=sa.BOOLEAN(), nullable=True)


def downgrade() -> None:
    op.alter_column("instance", "public", existing_type=sa.BOOLEAN(), nullable=False)
    op.drop_constraint(
        op.f("fk_account_instance_instance_id_instance"),
        "account_instance",
        type_="foreignkey",
    )
