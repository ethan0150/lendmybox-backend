from pydantic import BaseModel
from datetime import datetime

class InstanceInfo(BaseModel):
    name: str
    defualtUser: str
    image: str
    sshKey: str
    createdAt: datetime
    expireAt: datetime
    ipv4: str
    ipv6: str

class InstanceList(BaseModel):
    instances: list[InstanceInfo]

class KeyInfo(BaseModel):
    key: str
    createdAt: datetime
    expireAt: datetime

class KeyList(BaseModel):
    keys: list[KeyInfo]

class UserMetrics(BaseModel):
    name: str
    instenceNames: list[str]
    storageUsage: int #bytes
    cpuTime: int #ms maybe?
    createdAt: datetime

class UserInfo(BaseModel):
    uid: int
    username: str
    createdAt: datetime
    instanceCreated: int
    insteaceDeleted: int

class Message(BaseModel):
    message: str

class ImgList(BaseModel):
    imgs: list[str]