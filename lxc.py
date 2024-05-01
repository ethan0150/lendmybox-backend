from datetime import datetime
import yaml
import asyncio
import pylxd
async def launchInstance(name: str, user: str, img: str, key: str) -> None:
    client = pylxd.Client()
    userdata_yaml = ''
    with open('init.yaml', 'r') as f:
        userdata_yaml = yaml.safe_load(f)
        f.seek(0)
        old = f.read()
        print(old)
    userdata_yaml['users'][0]['name'] = user
    userdata_yaml['users'][0]['ssh_authorized_keys'] = [key]
    userdata = yaml.safe_dump(userdata_yaml, line_break='\n')
    userdata = f'#cloud-config\n{userdata}'
    print(userdata_yaml)
    print(userdata)
    cfg = {'name': name,
           'source':
                {'type': 'image',
                 'alias': img,
                 'mode': 'pull',
                 'protocol': 'simplestreams',
                 'server':'https://images.linuxcontainers.org'},
            'config': {'user.user-data': userdata }}
    ins = await asyncio.to_thread(client.instances.create, cfg, wait=True)
    ins.start()
    return
async def rmInstance(name:str):
    pass
async def addSSHKey(key: str, instanceName: str | None = None, expireAt: datetime | None = None):
    pass
async def deleteSSHKey(fp: str, instanceName: str | None = None):
    pass
async def setSSHPort(instanceName: str, port: int):
    pass
async def getIP(instanceName: str):
    pass