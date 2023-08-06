from sqlmodel import create_engine

from lnhub_rest.schema.migrations.settings import SUPABASE_DB_URL

if SUPABASE_DB_URL != "no-admin-password":
    engine = create_engine(SUPABASE_DB_URL)  # enqine
else:
    engine = None
