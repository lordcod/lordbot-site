import aiohttp
from resources import info
import orjson
api = info.api

async def getOAuthTokens(code):
    data = {
        'client_id': info.client.id,
        'client_secret': info.client.secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': info.redirect_uri
    } 
    data = orjson.dumps(data)
    headers={'Content-Type':'application/x-www-form-urlencoded'}
    url = f'{api}/oauth2/token'
    async with aiohttp.ClientSession() as session:
        res = await session.post(url,data=data,headers=headers)
        json = await res.json()
        return json

async def updateTokens(tokens):
    data = {
        'client_id': info.client.id,
        'client_secret': info.client.secret,
        'grant_type': 'refresh_token',
        'refresh_token': tokens['refresh_token'],
        'redirect_uri': info.redirect_uri
    }
    data = orjson.dumps(data)
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
    url = f'{api}/oauth2/token'
    async with aiohttp.ClientSession() as session:
        res = await session.post(url,data=data,headers=headers)
        json = await res.json()
        return json

async def getUserDate(tokens):
    url = f'{api}/users/@me'
    headers={"Authorization": "Bearer "+tokens['access_token']}
    async with aiohttp.ClientSession() as session:
        res = await session.get(url,headers=headers)
        json = await res.json()
        return json

async def pushMetadate(metadata,tokens):
    data = metadata
    headers={
        'Authorization': 'Bearer '+tokens['access_token'],
        'Content-Type': 'application/json',
    }
    url = f'{api}/users/@me/applications/{client_id}/role-connection'
    async with aiohttp.ClientSession() as session:
        res = await session.post(url,data=data,headers=headers)
        json = await res.json()
        return json

async def getMetadata(tokens):
    headers= {
        'Authorization': 'Bearer '+tokens['access_token'],
        }
    url = f'{api}/users/@me/applications/{client_id}/role-connection'
    async with aiohttp.ClientSession() as session:
        res = await session.put(url,headers=headers)
        json = await res.json()
        return json

async def getGuilds(tokens):
    url = f'{api}/users/@me/guilds'
    params = {'limit':200}
    headers={"Authorization":f"Bearer {tokens['access_token']}",'Content-Type': 'application/json'}
    async with aiohttp.ClientSession() as session:
        res = await session.get(url,params=params,headers=headers)
        jsons = await res.json()
        return jsons

async def getGuildMember(guild_id,member_id):
    url=f'{api}/guilds/{guild_id}/members/{member_id}'
    headers={"Authorization": f'Bot {info.token}',"Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        res = await session.get(url,headers=headers)
        json = await res.json()
        return json

async def isBotGuild(guild_id):
    res = await getGuildMember(guild_id,"1095713975532007434")
    if 'code' not in res:
        return True
    return False

async def addGuild(guild_id,user_id,tokens):
    url=f'{api}/guilds/{guild_id}/members/{user_id}'
    data={'access_token':tokens['access_token']}
    data = orjson.dumps(data)
    headers={"Authorization": f'Bot {info.token}',"Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        res = await session.put(url,data=data,headers=headers)
        json = await res.json()
        return json

async def editPermissionCommand(guild_id,command_id,value,tokens):
    url = f'{api}/applications/{client_id}/guilds/{guild_id}/commands/{command_id}/permissions'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        "Authorization":f"Bearer {tokens['access_token']}"
    }   
    data = {
        'permissions':[
            {'id': guild_id, 'type': 1, 'permission': value}
        ]
    }
    data = orjson.dumps(data)
    async with aiohttp.ClientSession() as session:
        res = await session.put(url,data=data,headers=headers)
        print(await res.json())
