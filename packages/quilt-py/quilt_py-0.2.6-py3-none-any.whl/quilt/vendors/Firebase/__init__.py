import os
import json
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials


cred = credentials.Certificate(json.loads(os.environ["FIREBASE_CERT"]))
client = firebase_admin.initialize_app(cred)


def update_user(
    auth_id: str,
    display_name: str = None,
    email: str = None,
    email_verified: bool = None,
    # phone_number: bool = None,
    photo_url: str = None,
    disabled: bool = None,
    custom_claims: dict[str, str] = None,
) -> auth.UserRecord:
    kwargs = {
        "display_name": display_name,
        "email": email,
        "photo_url": photo_url,
        "disabled": disabled,
        "custom_claims": custom_claims,
    }
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    return auth.update_user(uid=auth_id, **kwargs)
