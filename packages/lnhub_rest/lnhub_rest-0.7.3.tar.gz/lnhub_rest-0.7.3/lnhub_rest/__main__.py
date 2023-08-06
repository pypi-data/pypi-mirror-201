import argparse
import os
from subprocess import run
from typing import Literal, Optional

import sqlmodel as sqm
from lamin_logger import logger
from packaging.version import parse as vparse
from typeguard import typechecked

description_cli = "Manage hub."
parser = argparse.ArgumentParser(
    description=description_cli, formatter_class=argparse.RawTextHelpFormatter
)
subparsers = parser.add_subparsers(dest="command")

# migrate
migr = subparsers.add_parser("migrate")
aa = migr.add_argument
aa("action", choices=["generate", "deploy"], help="Generate migration.")
aa(
    "--breaks-lndb",
    choices=["y", "n"],
    default=None,
    help="Specify whether migration will break lndb (y/n).",
)

# run
r = subparsers.add_parser("run")

# test
t = subparsers.add_parser("test")

# jupyter lab
j = subparsers.add_parser("jupyter")

# parse args
args = parser.parse_args()

# Helpers to check environment variables


def check_lamin_env():
    response = input("Choose an environment (local/staging/prod): ")

    if response not in ["local", "staging", "prod"]:
        raise SystemExit(
            f"Error: '{response}' is not a valid choice, choose local, staging or prod."
        )

    if "LAMIN_ENV" in os.environ:
        lamin_env = os.environ["LAMIN_ENV"]
    else:
        raise SystemExit(
            "Error: Current LAMIN_ENV is not set"
            f", run 'export LAMIN_ENV={response}' and try again."
        )

    if lamin_env != response:
        raise SystemExit(
            f"Error: Current LAMIN_ENV is set on {lamin_env}"
            f", run 'export LAMIN_ENV={response}' and try again."
        )

    return lamin_env


def check_env_ln_server_deploy():
    if "LN_SERVER_DEPLOY" not in os.environ:
        raise SystemExit(
            "Current LN_SERVER_DEPLOY is not set"
            ", run 'export LN_SERVER_DEPLOY=1' and try again."
        )


def check_env_lnhub_pg_password(lamin_env: Literal["local", "staging", "prod"]):
    if lamin_env == "staging":
        if "LNHUB_STAGING_PG_PASSWORD" not in os.environ:
            raise SystemExit("Current LNHUB_STAGING_PG_PASSWORD is not set.")
    elif lamin_env == "prod":
        if "LNHUB_PROD_PG_PASSWORD" not in os.environ:
            raise SystemExit("Current LNHUB_PROD_PG_PASSWORD is not set.")


def check_env_supabase_url(lamin_env: Literal["local", "staging", "prod"]):
    if lamin_env == "staging":
        if "SUPABASE_STAGING_URL" not in os.environ:
            raise SystemExit("Current SUPABASE_STAGING_URL is not set.")
    elif lamin_env == "prod":
        if "SUPABASE_PROD_URL" not in os.environ:
            raise SystemExit("Current SUPABASE_PROD_URL is not set.")


def check_env_supabase_anon_key(lamin_env: Literal["local", "staging", "prod"]):
    if lamin_env == "staging":
        if "SUPABASE_STAGING_ANON_KEY" not in os.environ:
            raise SystemExit("Current SUPABASE_STAGING_ANON_KEY is not set.")


def check_env_supabase_service_role_key(lamin_env: Literal["local", "staging", "prod"]):
    if lamin_env == "staging":
        if "SUPABASE_STAGING_SERVICE_ROLE_KEY" not in os.environ:
            raise SystemExit("Current SUPABASE_STAGING_SERVICE_ROLE_KEY is not set.")
    elif lamin_env == "prod":
        if "SUPABASE_PROD_SERVICE_ROLE_KEY" not in os.environ:
            raise SystemExit("Current SUPABASE_PROD_SERVICE_ROLE_KEY is not set.")


# CLI


def generate():
    run(
        "alembic --config lnhub_rest/schema/alembic.ini --name cbwk revision"
        " --autogenerate -m 'vX.X.X.'",
        shell=True,
    )


@typechecked
def deploy(breaks_lndb: Optional[Literal["y", "n"]] = None):
    from lndb import settings

    from lnhub_rest._engine import engine
    from lnhub_rest.schema import __version__, _migration
    from lnhub_rest.schema.versions import version_cbwk

    if len(__version__.split(".")) != 3:
        raise RuntimeError("Your __version__ string is not of form X.X.X")

    if breaks_lndb is None:
        raise SystemExit("Error: Pass --breaks-lndb y or --breaks-lndb n")

    lamin_env = check_lamin_env()
    if lamin_env == "local":
        raise SystemExit(
            "Execute ./docs/migration/01-migration.ipynb to perform migration on local"
            " supabase."
        )
    check_env_ln_server_deploy()
    check_env_lnhub_pg_password(lamin_env)

    if breaks_lndb:
        response = input(
            "Have you ensured that lndb and lamindb have releases on PyPI that users"
            " can pull?"
        )
        if response == "y":
            pass
        else:
            raise SystemExit(
                "Please test thoroughly and prepare releases for lndb and lamindb.\n"
                "Pin lnhub_rest in lamindb, set a lower bound in lndb."
            )

    if settings.user.handle.startswith(("test", "static-test")):
        raise SystemExit("Error: Log in with your developer handle, e.g., falexwolf")

    # check that a release was made
    with sqm.Session(engine) as ss:
        deployed_v = ss.exec(
            sqm.select(version_cbwk.v)
            .order_by(version_cbwk.v.desc())  # type: ignore
            .limit(1)
        ).one()
    if deployed_v == __version__:
        raise SystemExit("Error: Make a new release before deploying the migration!")
    if vparse(deployed_v) > vparse(__version__):
        raise RuntimeError(
            "The new version has to be greater than the deployed version."
        )

    process = run(
        "alembic --config lnhub_rest/schema/alembic.ini --name cbwk upgrade head",
        shell=True,
    )
    if process.returncode == 0:
        with sqm.Session(engine) as ss:
            ss.add(
                version_cbwk(
                    v=__version__,
                    migration=_migration,
                    user_id=settings.user.id,
                    breaks_lndb=(breaks_lndb == "y"),
                )
            )
            ss.commit()

        logger.success("Successfully migrated hub.")


def run_server():
    lamin_env = check_lamin_env()
    check_env_supabase_url(lamin_env)
    check_env_supabase_anon_key(lamin_env)

    run(
        "python3 ./lnhub_rest/main.py",
        shell=True,
    )


def test():
    lamin_env = check_lamin_env()
    check_env_ln_server_deploy()
    if lamin_env == "local":
        # Needed to mirror the production schema
        # to apply local migration
        check_env_lnhub_pg_password("prod")
        # Needed to enable sign in and signup tests
        # to be performed on staging environment
        check_env_supabase_url("staging")
        check_env_supabase_anon_key("staging")
        check_env_supabase_service_role_key("staging")
    else:
        check_env_lnhub_pg_password(lamin_env)
        check_env_supabase_url(lamin_env)
        check_env_supabase_anon_key(lamin_env)
        check_env_supabase_service_role_key(lamin_env)

    run(
        "python3 -m nox",
        shell=True,
    )


def jupyter():
    lamin_env = check_lamin_env()

    if lamin_env == "local":
        # Needed to run the local migration
        # through migration notebook
        check_env_ln_server_deploy()
        # Needed to mirror the production schema
        # to apply local migration
        check_env_lnhub_pg_password("prod")
        # Needed to enable sign in and signup tests
        # to be performed on staging environment
        check_env_supabase_url("staging")
        check_env_supabase_anon_key("staging")
        check_env_supabase_service_role_key("staging")
    else:
        check_env_supabase_url(lamin_env)
        check_env_supabase_anon_key(lamin_env)
        check_env_supabase_service_role_key(lamin_env)

    run(
        "jupyter lab",
        shell=True,
    )


def main():
    if args.command == "migrate":
        if args.action == "generate":
            generate()
        if args.action == "deploy":
            deploy(breaks_lndb=args.breaks_lndb)
    elif args.command == "run":
        run_server()
    elif args.command == "test":
        test()
    elif args.command == "jupyter":
        jupyter()
    else:
        logger.error("Invalid command. Try `lndb -h`.")
        return 1
