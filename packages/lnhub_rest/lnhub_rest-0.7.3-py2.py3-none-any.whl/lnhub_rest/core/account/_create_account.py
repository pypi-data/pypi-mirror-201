from typing import Optional, Union

from postgrest.exceptions import APIError

from lnhub_rest._sbclient import connect_hub_with_auth
from lnhub_rest.core.account._crud import sb_insert_account
from lnhub_rest.utils._access_token import extract_id
from lnhub_rest.utils._id import base62


def create_account(
    _access_token: str,
    handle: str,
    organization: Optional[bool] = False,
) -> Union[None, str]:
    hub = connect_hub_with_auth(access_token=_access_token)
    try:
        lnid = base62(8)
        id = extract_id(_access_token)

        account = sb_insert_account(
            {
                "id": id,
                "user_id": id if not organization else None,
                "lnid": lnid,
                "handle": handle,
            },
            hub,
        )
        assert account is not None

        return None
    except APIError as api_error:
        usermeta_pkey_error = (
            'duplicate key value violates unique constraint "usermeta_pkey"'
        )
        if api_error.message == usermeta_pkey_error:
            return "handle-exists-already"
        raise api_error
    except Exception as e:
        raise e
    finally:
        hub.auth.sign_out()
