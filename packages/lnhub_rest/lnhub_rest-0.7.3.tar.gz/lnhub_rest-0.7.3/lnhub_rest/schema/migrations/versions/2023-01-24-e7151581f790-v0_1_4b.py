"""v0.1.4b.

Revision ID: e7151581f790
Revises: c13c9dd0f3ae
Create Date: 2023-01-24 20:34:28.140561

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e7151581f790"
down_revision = "c13c9dd0f3ae"
branch_labels = None
depends_on = None


sql = """
drop trigger on_auth_user_created on auth.users;
drop function public.handle_new_user;
"""


def upgrade() -> None:
    op.execute(sql)
    op.drop_table("auxuser")


def downgrade() -> None:
    pass
