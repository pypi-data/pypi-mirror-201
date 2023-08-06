import os
import json
import httpx
from quilt.vendors.Firebase import auth
from quilt import logs

logger = logs.create_logger(__name__)


def id_token_from_custom_token(custom_token: bytes) -> bytes:
    logger.debug("getting custom token from jwt_creator_url")
    res = httpx.post(
        os.environ["JWT_CREATOR_URL"],
        json={
            "customToken": custom_token.decode(),
            "firebaseConfig": json.loads(os.environ["FIREBASE_FRONTEND_CONFIG"]),
        },
        timeout=10,
    )
    return res.content


def get_user(phone_number: str) -> auth.UserRecord:
    return auth.get_user_by_phone_number(phone_number)


def bearer_token_from_auth_id(auth_id: str) -> bytes:
    custom_token = auth.create_custom_token(uid=auth_id)
    return id_token_from_custom_token(custom_token)


def bearer_token_from_phone_number(phone_number: str) -> bytes:
    try:
        auth_user = auth.get_user_by_phone_number(phone_number)
        logger.debug(f"got existing auth user with phone_number={phone_number}")
    except auth.UserNotFoundError:
        auth_user = auth.create_user(phone_number=phone_number)
        logger.debug(f"created auth user with phone_number={phone_number}")
    return bearer_token_from_auth_id(auth_user.uid)
