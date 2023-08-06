import os
import hmac
from fastapi import APIRouter, Header, Depends, HTTPException
from quilt.models import PhoneNumber
from app import settings, Env
from . import logic

router = APIRouter()


def is_valid_header(secret_key: str = Header(...)) -> None:
    if not hmac.compare_digest(secret_key, os.environ["CUSTOM_BEARER_SECRET_KEY"]):
        raise HTTPException(status_code=401, detail="Invalid key.")


def is_sandbox() -> None:
    if settings.env != Env.SANDBOX:
        raise HTTPException(status_code=500, detail="Sandbox only.")


@router.post("/bearer_token_from_phone", response_model=str)
def get_bearer_token_from_phone_number(  # type: ignore
    phone_number: PhoneNumber,
    _=Depends(is_valid_header),
    __=Depends(is_sandbox),
) -> str:
    token = logic.bearer_token_from_phone_number(phone_number=phone_number)
    return token.decode("utf-8")


@router.post("/bearer_token_from_auth_id", response_model=str)
def get_bearer_token_from_auth_id(  # type: ignore
    auth_id: str,
    _=Depends(is_valid_header),
    __=Depends(is_sandbox),
) -> str:
    token = logic.bearer_token_from_auth_id(auth_id=auth_id)
    return token.decode("utf-8")
