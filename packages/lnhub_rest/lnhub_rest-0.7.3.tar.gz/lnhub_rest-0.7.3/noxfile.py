import os

import nox

nox.options.reuse_existing_virtualenvs = True

lamin_env = "local"
if "GITHUB_REF_NAME" in os.environ:
    if os.environ["GITHUB_REF_NAME"] == "main":
        lamin_env = "prod"
    # if running in GI and branch is not main, then always use staging credentials
    else:
        lamin_env = "staging"
elif "LAMIN_ENV" in os.environ:
    lamin_env = os.environ["LAMIN_ENV"]


@nox.session
def lint(session: nox.Session) -> None:
    session.install("pre-commit")
    session.run("pre-commit", "install")
    session.run("pre-commit", "run", "--all-files")


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def build(session):
    session.install(".[dev,test]")
    session.run(
        "pytest",
        "-s",
        "--cov=lnhub_rest",
        "--cov-append",
        "--cov-report=term-missing",
        env={"LN_SERVER_DEPLOY": "1", "LAMIN_ENV": lamin_env},
    )
    # session.run("coverage", "xml")


@nox.session
def supabase_stop(session: nox.Session) -> None:
    session.run("supabase", "db", "reset", external=True)
    session.run("supabase", "stop", external=True)
