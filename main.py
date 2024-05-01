from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from jose import JWTError

from dotenv import load_dotenv
load_dotenv()

from database import *
from service import *
from requestSchema import *
from responseSchema import *

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

imgSet = None
imgList = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global imgSet, imgList
    imgSet, imgList = await getImgInfo()
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)
get_cred = HTTPBearer()
sched = AsyncIOScheduler(jobstores={'default':MemoryJobStore()})

@sched.scheduled_job('interval', seconds=300)
async def refreshImg():
    global imgSet, imgList
    imgSet, imgList = await getImgInfo()

@app.post("/register", response_model=UID)
async def register(loginCred: LoginCred, db: AsyncSession = Depends(get_db)):
    uid = await register_user(db, loginCred)
    if not uid:
        raise HTTPException(status_code=400, detail="Username Already exists")
    
    return UID(uid=uid)

@app.post("/login")
async def login(loginCred: LoginCred, db: AsyncSession = Depends(get_db)):
    uid = await verifyPass(db, loginCred.username, loginCred.password)
    if not uid:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    try:
        token = await create_access_token(uid)
    except JWTError:
        raise HTTPException(status_code=500, detail="Failed to create access token")
    
    return Token(access_token=token, token_type="bearer")


@app.get("/user", response_model=UserInfo)
async def getUser(cred: HTTPAuthorizationCredentials = Depends(get_cred), 
                  db: AsyncSession = Depends(get_db)):
    uid = await parseUid(cred.credentials)
    user = await get_user(db, uid)
    return UserInfo(uid=uid,
                    username=user.username,
                    createdAt=user.createdAt,
                    instanceCreated=user.instanceCreated,
                    insteaceDeleted=user.instanceDeleted)

@app.post("/user", response_model=UID, status_code=201)
async def createUser(loginCred: LoginCred, db: AsyncSession = Depends(get_db)):
    uid = await register_user(db, loginCred)
    if not uid:
        raise HTTPException(status_code=400, detail="Username Already exists")
    return UID(uid=uid)

@app.delete("/user", response_model=Message)
async def deleteUser(cred: HTTPAuthorizationCredentials = Depends(get_cred),
                     db: AsyncSession = Depends(get_db)):
    uid = await parseUid(cred.credentials)
    await delete_user(db, uid)
    return Message(message=f'User {uid} has been deleted.')

@app.get("/imglist", response_model=ImgList)
async def getImgList():
    return ImgList(imgs=imgList)

@app.get("/instance", response_model=InstanceInfo)
async def getInstance(req: InstanceName, db: AsyncSession = Depends(get_db)):
    pass

@app.get("/instance/all", response_model=InstanceList)
async def getAllInstance(db: AsyncSession = Depends(get_db)):
    pass

@app.post("/instance")
async def createInstance(req: InstancePost, db: AsyncSession = Depends(get_db)):
    await setup_instance(db, req.name, req.defaultUser, req.image, req.sshKey)

@app.delete("/instance")
async def deleteInstance(req: InstanceName, db: AsyncSession = Depends(get_db)):
    pass

@app.get("/sshkey", response_model=KeyInfo)
async def getSSHKey(req: KeyFP, db: AsyncSession = Depends(get_db)):
    pass

@app.get("/sshkey/all", response_model=KeyList)
async def getAllSSHKey(req: InstanceName, db: AsyncSession = Depends(get_db)):
    pass

@app.post("/sshkey")
async def createSSHKey(req: KeyPost, db: AsyncSession = Depends(get_db)):
    pass

@app.delete("/sshkey")
async def deleteSSHKey(req: KeyFP, db: AsyncSession = Depends(get_db)):
    pass