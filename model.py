from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Instance(Base):
    __tablename__ = "instance"

    name = Column(String(63), primary_key=True, index=True)
    uid = Column(Integer, index=True)
    sshPort = Column(Integer, unique=True)
    image = Column(String(256))
    defualtUser = Column(String(128))
    createdAt = Column(DateTime, default=func.now())
    expireAt = Column(DateTime)

class User(Base): 
    __tablename__ = "user"

    uid = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    createdAt = Column(DateTime, default=func.now())
    instanceCreated = Column(Integer, default=0)
    instanceDeleted = Column(Integer, default=0)
    hashedPass = Column(String(100))

class SSHKey(Base):
    __tablename__ = "sshkey"

    uid = Column(Integer, index=True)
    instanceName = Column(String(63), primary_key=True, nullable=True, index=True)
    fp = Column(String(63), primary_key=True, unique=True)
    key = Column(String(2048))
    createdAt = Column(DateTime, default=func.now())
    expireAt = Column(DateTime)