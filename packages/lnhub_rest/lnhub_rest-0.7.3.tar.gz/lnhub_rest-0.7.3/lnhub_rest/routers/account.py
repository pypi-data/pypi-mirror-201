from typing import Annotated, Union

from fastapi import APIRouter, Header, Query

from ..core.account._create_account import create_account as create_account_base
from ..core.account._update_account import update_account as update_account_base
from .utils import extract_access_token, get_supabase_client, supabase_client

router = APIRouter(prefix="/account")


@router.get("/{id}")
def get_account_by_id(id: str):
    data = supabase_client.table("account").select("*").eq("id", id).execute().data
    return data[0] if len(data) > 0 else None


@router.get("/handle/{handle}")
def get_account_by_handle(handle: str):
    data = (
        supabase_client.table("account").select("*").eq("handle", handle).execute().data
    )
    return data[0] if len(data) > 0 else None


@router.get("/resources/instances/{handle}")
def get_account_instances(
    handle: str, authentication: Union[str, None] = Header(default=None)
):
    access_token = extract_access_token(authentication)
    supabase_client = get_supabase_client(access_token)

    try:
        account_instances = (
            supabase_client.table("account")
            .select(
                """account_instance(*, instance(
                *, account!fk_instance_account_id_account(handle, id)))""".replace(
                    "\n", ""
                )
            )
            .eq("handle", handle)
            .execute()
            .data[0]["account_instance"]
        )

        return account_instances

    finally:
        supabase_client.auth.sign_out()


@router.post("/")
def create_account(
    handle: str,
    organization: Union[bool, None] = False,
    authentication: Union[str, None] = Header(default=None),
):
    access_token = extract_access_token(authentication)
    message = create_account_base(
        handle=handle,
        organization=organization,
        _access_token=access_token,
    )
    if message is None:
        return "success"
    return message


@router.put("/")
def update_account(
    handle: Union[str, None] = None,
    name: Union[str, None] = None,
    bio: Union[str, None] = None,
    github_handle: Union[str, None] = None,
    linkedin_handle: Union[str, None] = None,
    twitter_handle: Union[str, None] = None,
    website: Union[str, None] = None,
    authentication: Union[str, None] = Header(default=None),
):
    access_token = extract_access_token(authentication)
    message = update_account_base(
        handle=handle,
        name=name,
        bio=bio,
        github_handle=github_handle,
        linkedin_handle=linkedin_handle,
        twitter_handle=twitter_handle,
        website=website,
        _access_token=access_token,
    )
    if message is None:
        return "success"
    return message


@router.get("/bulk/avatars")
def get_account_avatars(lnids: Annotated[list[str], Query()]):
    data = (
        supabase_client.table("account")
        .select("lnid, avatar_url")
        .in_("lnid", lnids)
        .execute()
        .data
    )
    return data if len(data) > 0 else []
