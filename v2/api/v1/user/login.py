from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from core.database import get_session
from models.admin import Admin
from models.common import Message
from models.login import Login
from utils.hash import check_hash

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/", response_model=Message)
async def login(
    *, session: Session = Depends(get_session), login: Login
) -> Message | HTTPException:

    statement = select(Admin).where(Admin.username == login.username)
    results = session.exec(statement)
    user = results.first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not check_hash(login.password, user.hash):
        raise HTTPException(status_code=401, detail="Unauthorized")

    return Message(message="ok")
