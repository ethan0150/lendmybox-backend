from pydantic import BaseModel
from datetime import datetime

class Username(BaseModel):
    username: str

class LoginCred(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UID(BaseModel):
    uid: int

class InstancePost(BaseModel):
    name: str
    defaultUser: str
    image: str
    sshKey: str

class KeyPost(BaseModel):
    instanceName: str | None
    key: str
    expireAt: datetime | None

class KeyFP(BaseModel):
    InstanceName: str | None
    fp: str

class InstanceName(BaseModel):
    name: str | None