from typing import Union

from fastapi import APIRouter, Header

from .._delete_instance import delete_instance as delete_instance_base
from .._init_instance import init_instance as init_instance_base
from ..core.instance._update_instance import update_instance as update_instance_base
from .account import get_account_by_handle
from .utils import (
    extract_access_token,
    get_account_permission_for_instance,
    get_supabase_client,
)

router = APIRouter(prefix="/instance")


@router.get("/{account_handle}/{name}")
def get_instance_by_name(
    account_handle: str,
    name: str,
    authentication: Union[str, None] = Header(default=None),
):
    access_token = extract_access_token(authentication)
    supabase_client = get_supabase_client(access_token)

    try:
        account = get_account_by_handle(account_handle)
        data = (
            supabase_client.table("instance")
            .select(
                "*, storage(root), account!fk_instance_account_id_account(handle, id))"
            )
            .eq("account_id", account["id"])
            .eq("name", name)
            .execute()
            .data
        )

        if len(data) > 0:
            instance = data[0]
            if authentication is not None:
                permission = get_account_permission_for_instance(
                    data[0]["id"], access_token
                )
            else:
                permission = None
        else:
            instance = None
            permission = None

        return {"instance": instance, "permission": permission}

    finally:
        supabase_client.auth.sign_out()


@router.get("/resources/accounts/{account_handle}/{name}")
def get_instance_accounts(
    account_handle: str,
    name: str,
    authentication: Union[str, None] = Header(default=None),
):
    access_token = extract_access_token(authentication)
    supabase_client = get_supabase_client(access_token)

    try:
        account = get_account_by_handle(account_handle)
        data = (
            supabase_client.table("instance")
            .select("""id, account_instance(*, account(*))""")
            .eq("account_id", account["id"])
            .eq("name", name)
            .execute()
            .data
        )
        if len(data) > 0:
            account_instances = data[0]["account_instance"]
            if authentication is not None:
                permission = get_account_permission_for_instance(
                    data[0]["id"], access_token
                )
            else:
                permission = None
        else:
            account_instances = None
            permission = None

        return {"accounts": account_instances, "permission": permission}

    finally:
        supabase_client.auth.sign_out()


@router.post("/")
def create_instance(
    account_handle: str,
    name: str,
    storage: str,
    db: Union[str, None] = None,
    schema: Union[str, None] = None,
    description: Union[str, None] = None,
    public: Union[bool, None] = None,
    authentication: Union[str, None] = Header(default=None),
):
    access_token = extract_access_token(authentication)
    message = init_instance_base(
        owner=account_handle,
        name=name,
        storage=storage,
        db=db,
        schema=schema,
        description=description,
        public=public,
        _access_token=access_token,
    )
    if message is None:
        return "success"
    return message


@router.delete("/")
def delete_instance(
    account_handle: str,
    name: str,
    authentication: Union[str, None] = Header(default=None),
):
    access_token = extract_access_token(authentication)
    message = delete_instance_base(
        owner=account_handle, name=name, _access_token=access_token
    )
    if message is None:
        return "success"
    return message


@router.put("/")
def update_instance(
    instance_id: str,
    account_id: Union[str, None] = None,
    public: Union[bool, None] = None,
    description: Union[str, None] = None,
    authentication: Union[str, None] = Header(default=None),
):
    access_token = extract_access_token(authentication)
    message = update_instance_base(
        instance_id=instance_id,
        account_id=account_id,
        public=public,
        description=description,
        _access_token=access_token,
    )
    if message is None:
        return "success"
    return message
