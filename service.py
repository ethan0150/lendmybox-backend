from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from os import getenv
from crud import *
from requestSchema import LoginCred, UID
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import logging
from lxc import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def register_user(db: AsyncSession, user_data: LoginCred) -> int | None:
    user = await get_user_by_username(db, user_data.username)
    if user:
        return None
    hash = pwd_context.hash(user_data.password)
    uid = await create_user(db, user_data.username, hash)
    return uid

async def delete_user(db: AsyncSession, uid: int) -> None:
    await delete_user_by_id(db, uid)

async def verifyPass(db: AsyncSession, username: str, password: str) -> int | None:
    user = await get_user_by_username(db, username)
    if not (user and pwd_context.verify(password, user.hashedPass)):
        return None
    return user.uid

async def create_access_token(uid: int, expires_delta: timedelta = timedelta(minutes=15)) -> str | None:
    to_encode = {"sub": str(uid)}
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(to_encode, key=getenv("SECRET_KEY"), algorithm=getenv("ALGORITHM"))
    except JWTError:
        raise
    return encoded_jwt

async def get_user(db: AsyncSession, uid: int) -> User:
    return await get_user_by_uid(db, uid)

async def verifyImg(img: str):
    pass

async def setup_instance(db: AsyncSession, name: str, user: str, img: str, sshKey: str) -> None:
    await launchInstance(name, user, img, sshKey)

async def parseUid(cred: str) -> int:
    token = jwt.decode(cred, getenv("SECRET_KEY"), getenv("ALGORITHM"))
    return int(token.get("sub"))

async def getImgInfo() -> tuple[set, list[str]]:
    proc = await asyncio.create_subprocess_exec(
        'incus', 'image', 'list', 'images:', 'architecture=amd64', 'type=container', '-c', 'l', '-f', 'csv',
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await proc.communicate()
    imgLines = out.decode().strip().splitlines()
    rets = set()
    retl = []
    for l in imgLines:
        if 'cloud' in l:
            stripped = l.split(' ', 1)[0]
            rets.add(stripped)
            retl.append(stripped)
    logging.info("Image list refresh complete.")
    return rets, retl