"""v0.1.4a.

This introduces an auxiliary user table needed to query the auth schema user table.

Revision ID: c13c9dd0f3ae
Revises: f7ba9352c706
Create Date: 2023-01-23 16:27:41.130937

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c13c9dd0f3ae"
down_revision = "f7ba9352c706"
branch_labels = None
depends_on = None


sql = """

create table public.auxuser (
  id uuid not null references auth.users on delete cascade,
  email text,
  created_at timestamp,
  primary key (id)
);

alter table public.auxuser enable row level security;

create function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.auxuser (id)
  values (new.id, new.email, new.created_at);
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

"""


def upgrade() -> None:
    op.execute(sql)
    # ORM and the SQL above differ in how they define the foreign key constraint,
    # hence, the following
    op.drop_constraint("auxuser_id_fkey", "auxuser", type_="foreignkey")
    op.create_foreign_key(
        "auxuser_id_fkey", "auxuser", "users", ["id"], ["id"], referent_schema="auth"
    )


def downgrade() -> None:
    pass
    # op.drop_table("auxuser")
