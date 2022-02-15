from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from api.v1.utils.admin import api_admin
from api.v1.utils.user import api_user
from core.database import get_session
from models.common import Message
from models.user import UserCreate

router = APIRouter(prefix="/register", tags=["register"])


@router.post("/", response_model=Message)
async def register(
    *, session: Session = Depends(get_session), register: UserCreate
) -> Message | HTTPException:

    db_user = api_user.get_by_username(session, register.username)
    db_admin = api_admin.get_by_username(session, register.username)

    if db_user or db_admin:
        raise HTTPException(status_code=409, detail="User already exist")

    db_user = api_user.create_user(session, register)

    return Message(message="ok")
