import os

try:
    PROD_URL = f"postgresql://postgres:{os.environ['LNHUB_PROD_PG_PASSWORD']}@db.laesaummdydllppgfchu.supabase.co:5432/postgres"  # noqa
except KeyError:
    PROD_URL = "no-admin-password"

try:
    STAGING_URL = f"postgresql://postgres:{os.environ['LNHUB_STAGING_PG_PASSWORD']}@db.amvrvdwndlqdzgedrqdv.supabase.co:5432/postgres"  # noqa
except KeyError:
    STAGING_URL = "no-admin-password"

LOCAL_URL = "postgresql://postgres:postgres@localhost:54322/postgres"

if "LAMIN_ENV" in os.environ:
    if os.environ["LAMIN_ENV"] == "staging":
        SUPABASE_DB_URL = STAGING_URL
    elif os.environ["LAMIN_ENV"] == "local":
        SUPABASE_DB_URL = LOCAL_URL
    else:
        SUPABASE_DB_URL = PROD_URL
else:
    SUPABASE_DB_URL = PROD_URL
