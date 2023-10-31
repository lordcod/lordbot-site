import aiohttp
from resources import info
import orjson


api = 'https://discord.com/api/v10'


async def getOAuthTokens(code):
    url = f'{api}/oauth2/token'
    data = {
        'client_id': info.dis_client_id,
        'client_secret': info.dis_client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': info.dis_redirect_uri
    } 
    headers = {'Content-Type':'application/x-www-form-urlencoded'}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url,data=data,headers=headers) as res:
            json = await res.json()
            return json

async def updateTokens(tokens):
    url = f'{api}/oauth2/token'
    data = {
        'client_id': info.dis_client_id,
        'client_secret': info.dis_client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': tokens['refresh_token'],
        'redirect_uri': info.dis_redirect_uri
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url,data=data,headers=headers) as res:
            json = await res.json()
            return json


async def getUserDate(tokens):
    url = f'{api}/users/@me'
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url,headers=headers) as res:
            json = await res.json()
            return json

async def pushMetadate(metadata,tokens):
    url = f'{api}/users/@me/applications/{info.dis_client_id}/role-connection'
    data = metadata
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Content-Type": "application/json",
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url,data=data,headers=headers) as res:
            json = await res.json()
            return json

async def getMetadata(tokens):
    url = f'{api}/users/@me/applications/{info.dis_client_id}/role-connection'
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.put(url,headers=headers) as res:
            json = await res.json()
            return json

async def getGuilds(tokens):
    url = f'{api}/users/@me/guilds'
    params={'limit':200}
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Content-Type": "application/json",
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url,params=params,headers=headers) as res:
            json = await res.json()
            return json

async def getGuildMember(guild_id,member_id):
    url=f'{api}/guilds/{guild_id}/members/{member_id}'
    headers = {
        "Authorization": f"Bearer {info.token}",
        "Content-Type": "application/json",
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url,headers=headers) as res:
            json = await res.json()
            return json

async def isBotGuild(guild_id):
    res = await getGuildMember(guild_id,info.dis_client_id)
    if 'code' not in res:
        return True
    return False

async def addGuild(guild_id,user_id,tokens):
    url = f'{api}/guilds/{guild_id}/members/{user_id}'
    data = {'access_token':tokens['access_token']},
    data=orjson.dumps(data)
    headers={
        "Authorization": f'Bot {info.token}',
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.put(url,data=data,headers=headers) as res:
            json = await res.json()
            return json
