import os
from typing import Optional, Tuple
from uuid import UUID, uuid4

from lnhub_rest import check_breaks_lndb_and_error
from lnhub_rest.core.storage._crud import sb_insert_storage, sb_select_storage_by_root

from ..._sbclient import connect_hub_with_auth


def add_storage(
    root: str, account_handle: str, _access_token: Optional[str] = None
) -> Tuple[Optional[UUID], Optional[str]]:
    from botocore.exceptions import ClientError

    from lnhub_rest.core.account._crud import sb_select_account_by_handle

    hub = connect_hub_with_auth(access_token=_access_token)
    try:
        check_breaks_lndb_and_error(hub)  # assumes that only called from within lndb
        validate_root_arg(root)
        # get account
        account = sb_select_account_by_handle(account_handle, hub)

        # check if storage exists already
        storage = sb_select_storage_by_root(root, hub)
        if storage is not None:
            return storage["id"], None

        # add storage
        if "LNHUB_NOT_USE_BOTO3" in os.environ:
            storage_region = None
        else:
            storage_region = get_storage_region(root)
        storage_type = get_storage_type(root)
        storage = sb_insert_storage(
            {
                "id": uuid4().hex,
                "account_id": account["id"],
                "root": root,
                "region": storage_region,
                "type": storage_type,
            },
            hub,
        )
        assert storage is not None

        return storage["id"], None
    except ClientError as exception:
        if exception.response["Error"]["Code"] == "NoSuchBucket":
            return None, "bucket-does-not-exists"
        else:
            return None, exception.response["Error"]["Message"]
    finally:
        hub.auth.sign_out()


def validate_root_arg(root: str) -> None:
    if not root.startswith(("s3://", "gs://")):
        raise ValueError("Only accept s3 and Google Cloud buckets.")


def get_storage_region(storage_root: str) -> Optional[str]:
    storage_root_str = str(storage_root)
    storage_region = None

    if storage_root_str.startswith("s3://"):
        import boto3

        response = boto3.client("s3").get_bucket_location(
            Bucket=storage_root_str.replace("s3://", "")
        )
        # returns `None` for us-east-1
        # returns a string like "eu-central-1" etc. for all other regions
        storage_region = response["LocationConstraint"]
        if storage_region is None:
            storage_region = "us-east-1"

    return storage_region


def get_storage_type(storage_root: str):
    if str(storage_root).startswith("s3://"):
        return "s3"
    elif str(storage_root).startswith("gs://"):
        return "gs"
    else:
        return "local"
